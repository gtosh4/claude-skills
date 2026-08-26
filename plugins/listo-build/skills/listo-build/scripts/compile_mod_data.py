"""Compile BG3 and enabled Listonomicon character-build data into SQLite.

The compiler reads the retail gameplay archives and active Mod Organizer profile,
then preserves every structured definition with its base-game archive or MO2 mod
source and effective load-order position. Media assets are indexed, not copied.

BG3 Forge supplies the PAK, LSF/LSJ, and binary localization decoders:

    python3 -m pip install "bg3forge[zstd]==0.2.0"
    python3 compile_mod_data.py /path/to/listo.sqlite
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
import argparse
import json
import os
import re
import sqlite3
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any


try:
    from bg3forge.pak.format import PakHeader as _forge_pak_header
    from bg3forge.pak.reader import PakReader as _forge_pak_reader
    from bg3forge.parsers.localization import parse_loca as _forge_parse_loca
    from bg3forge.parsers.resource import parse_resource as _forge_parse_resource
except ImportError:
    _forge_pak_header = None
    _forge_pak_reader = None
    _forge_parse_loca = None
    _forge_parse_resource = None

DEFAULT_INSTALL_ROOT = Path("/mnt/mercury/Games/Listonomicon")
DEFAULT_PROFILE = "Listonomicon"
DEFAULT_GAME_DATA = Path("/mnt/mercury/Steam/steamapps/common/Baldurs Gate 3/Data")

BASE_GAME_ARCHIVES = {
    "game.pak",
    "gustav.pak",
    "gustavdev.pak",
    "gustavx.pak",
    "honour.pak",
    "honourx.pak",
    "shared.pak",
    "shareddev.pak",
}

# Resource directories that define character options or the mechanics they reference.
GAMEPLAY_RESOURCE_PARTS = {
    "ActionResourceDefinitions",
    "Backgrounds",
    "CharacterCreation",
    "CharacterCreationPresets",
    "ClassDescriptions",
    "EquipmentSettings",
    "EquipmentTypes",
    "Feats",
    "Gods",
    "Levelmaps",
    "Lists",
    "Origins",
    "Progressions",
    "Races",
    "RootTemplates",
    "Tags",
}
GAMEPLAY_RESOURCE_PARTS_CASEFOLD = {part.casefold() for part in GAMEPLAY_RESOURCE_PARTS}

_NEW_RECORD = re.compile(
    r'^\s*new\s+(entry|treasuretable|itemcombination|itemcombinationresult)\s+"((?:\\.|[^"\\])*)"',
    re.IGNORECASE,
)
_QUOTED = re.compile(r'"((?:\\.|[^"\\])*)"')
_NON_IDENTIFIER = re.compile(r"[^a-z0-9]+")
_CAMEL_BOUNDARY = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")


@dataclass(frozen=True)
class Module:
    uuid: str
    name: str | None
    folder: str | None
    load_order: int | None


@dataclass(frozen=True)
class Origin:
    source: str
    source_kind: str
    profile_order: int | None
    load_order: int | None
    archive_priority: int
    pak_path: str
    module: Module | None


@dataclass(frozen=True)
class Record:
    record_type: str
    name: str | None
    uuid: str | None
    using: str | None
    data: dict[str, Any]
    raw: str | None = None

@dataclass(frozen=True)
class PakJob:
    path: Path
    source: str
    source_kind: str
    profile_order: int | None
    default_load_order: int | None
    relative_pak: str
    by_uuid: dict[str, Module]
    by_folder: dict[str, Module]


@dataclass(frozen=True)
class ExtractedResource:
    origin: Origin
    entry: str
    compressed_size: int
    uncompressed_size: int
    kind: str
    records: tuple[Record, ...]
    status: str
    error: str | None


@dataclass(frozen=True)
class ExtractedPak:
    job: PakJob
    load_rows: frozenset[tuple[Any, ...]]
    resources: tuple[ExtractedResource, ...]


def _decode_quoted(value: str) -> str:
    """Decode the two escapes used by Stats text without inventing others."""
    return value.replace(r"\"", '"').replace(r"\\", "\\")


def _quoted_values(line: str) -> list[str]:
    return [_decode_quoted(match.group(1)) for match in _QUOTED.finditer(line)]


def _put_repeated(mapping: dict[str, Any], key: str, value: Any) -> None:
    previous = mapping.get(key)
    if previous is None:
        mapping[key] = value
    elif isinstance(previous, list):
        previous.append(value)
    else:
        mapping[key] = [previous, value]


def parse_stats(text: str) -> Iterator[Record]:
    """Yield Stats and treasure-table records from a generated-data text file."""
    lines = text.splitlines(keepends=True)
    starts = [index for index, line in enumerate(lines) if _NEW_RECORD.match(line)]
    starts.append(len(lines))

    for position, start in enumerate(starts[:-1]):
        end = starts[position + 1]
        raw = "".join(lines[start:end])
        header = _NEW_RECORD.match(lines[start])
        assert header is not None
        declaration = header.group(1)
        name = _decode_quoted(header.group(2))
        record_type = None if declaration.lower() == "entry" else _camel_type(declaration)
        using = None
        fields: dict[str, Any] = {}
        directives: list[dict[str, Any]] = []

        for line in lines[start + 1 : end]:
            command = line.lstrip().split(None, 1)[0].lower() if line.strip() else ""
            values = _quoted_values(line)
            if command == "type" and values:
                record_type = values[0]
            elif command == "using" and values:
                using = values[0]
            elif command == "data" and len(values) >= 2:
                _put_repeated(fields, values[0], values[1])
            elif command and not line.lstrip().startswith(("//", "/*", "*")):
                directives.append({"command": command, "values": values, "text": line.strip()})

        if directives:
            fields["_directives"] = directives
        yield Record(record_type or "StatsEntry", name, None, using, fields, raw)


def _camel_type(value: str) -> str:
    known = {
        "treasuretable": "TreasureTable",
        "itemcombination": "ItemCombination",
        "itemcombinationresult": "ItemCombinationResult",
    }
    return known.get(value.lower(), "".join(part.capitalize() for part in value.split("_")))


def _attribute_value(attribute: ET.Element) -> Any:
    result = dict(attribute.attrib)
    result.pop("id", None)
    if set(result) == {"value"}:
        return result["value"]
    return result


def _node_data(node: ET.Element) -> dict[str, Any]:
    attributes: dict[str, Any] = {}
    for attribute in node.findall("./attribute"):
        key = attribute.get("id")
        if key:
            _put_repeated(attributes, key, _attribute_value(attribute))

    children = [_node_data(child) for group in node.findall("./children") for child in group.findall("./node")]
    result: dict[str, Any] = {"node_type": node.get("id"), "attributes": attributes}
    if children:
        result["children"] = children
    text = (node.text or "").strip()
    if text:
        result["text"] = text
    return result


def _plain_attribute(attributes: dict[str, Any], key: str) -> str | None:
    value = attributes.get(key)
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        candidate = value.get("value") or value.get("handle")
        return candidate if isinstance(candidate, str) else None
    return None


def _record_type(node_type: str | None, entry: str | None) -> str:
    if node_type == "GameObjects" and entry and "/roottemplates/" in entry.lower():
        return "RootTemplate"
    return node_type or "LsxNode"


def parse_lsx(payload: bytes, entry: str | None = None) -> Iterator[Record]:
    """Yield top-level records from an XML Larian resource."""
    root = ET.fromstring(payload)
    for region in root.findall(".//region"):
        containers = region.findall("./node/children")
        nodes = [node for container in containers for node in container.findall("./node")]
        if not nodes:
            nodes = region.findall("./node")
        for node in nodes:
            data = _node_data(node)
            attributes = data["attributes"]
            name = _plain_attribute(attributes, "Name")
            uuid = _plain_attribute(attributes, "UUID") or _plain_attribute(attributes, "MapKey")
            yield Record(_record_type(node.get("id"), entry), name or uuid, uuid, None, data)


def _require_bg3forge() -> None:
    if (
        _forge_pak_header is None
        or _forge_pak_reader is None
        or _forge_parse_resource is None
        or _forge_parse_loca is None
    ):
        raise RuntimeError(
            'BG3 Forge 0.2.0 is required for PAK, LSF/LSJ, and .loca data; '
            'install it with: python3 -m pip install "bg3forge[zstd]==0.2.0"'
        )


def _forge_attribute_data(attribute: Any) -> dict[str, Any]:
    result = {"type": attribute.type}
    if attribute.value is not None:
        result["value"] = attribute.value
    if attribute.handle is not None:
        result["handle"] = attribute.handle
    if attribute.version is not None:
        result["version"] = attribute.version
    return result


def _forge_node_data(node: Any) -> dict[str, Any]:
    result: dict[str, Any] = {
        "node_type": node.id,
        "attributes": {key: _forge_attribute_data(value) for key, value in node.attributes.items()},
    }
    if node.key is not None:
        result["key"] = node.key
    if node.children:
        result["children"] = [_forge_node_data(child) for child in node.children]
    return result


def _parse_binary_document(payload: bytes) -> Any:
    try:
        return _forge_parse_resource(payload)
    except ValueError as original:
        # Some older authoring tools wrote version 6 LSF files with the
        # version 5 metadata layout. BG3 accepts them; Forge correctly parses
        # the same bytes when told which layout is actually present.
        if (
            payload[:4] == b"LSOF"
            and int.from_bytes(payload[4:8], "little") == 6
            and len(payload) >= 57
            and payload[48] & 0x0F in {0, 1, 2, 3}
            and payload[56] & 0x0F not in {0, 1, 2, 3}
        ):
            patched = payload[:4] + (5).to_bytes(4, "little") + payload[8:]
            try:
                return _forge_parse_resource(patched)
            except ValueError:
                pass
        raise original


def parse_binary_resource(payload: bytes, entry: str) -> Iterator[Record]:
    _require_bg3forge()
    document = _parse_binary_document(payload)
    for root in document.regions.values():
        nodes = root.children or [root]
        for node in nodes:
            data = _forge_node_data(node)
            name = node.get("Name")
            uuid = node.get("UUID") or node.get("MapKey")
            yield Record(_record_type(node.id, entry), name or uuid, uuid, None, data)


def parse_localization(payload: bytes, binary: bool = False) -> Iterator[Record]:
    if binary:
        _require_bg3forge()
        for content in _forge_parse_loca(payload):
            handle = content.key.split(";", 1)[0]
            yield Record(
                "Localization",
                handle,
                handle,
                None,
                {"text": content.text, "version": content.version, "key": content.key},
            )
        return

    try:
        root = ET.fromstring(payload)
    except ET.ParseError:
        # Shipped localization includes both malformed named entities and
        # files containing loose <content> fragments without a root element.
        repaired = payload.replace(b"&gt>", b"&gt;").replace(b"&lt<", b"&lt;")
        repaired = re.sub(rb"&(lt|gt|amp|quot|apos)(?!;)", rb"&\1;", repaired)
        try:
            root = ET.fromstring(repaired)
        except ET.ParseError:
            fragment = re.sub(rb"<\?xml[^>]*\?>", b"", repaired, count=1)
            root = ET.fromstring(b"<contentList>" + fragment + b"</contentList>")
    for content in root.findall(".//content"):
        handle = content.get("contentuid") or content.get("contentUid")
        data = {"text": "".join(content.itertext())}
        for key, value in content.attrib.items():
            if key.lower() != "contentuid":
                data[key] = value
        yield Record("Localization", handle, handle, None, data)


def parse_profile(path: Path) -> list[tuple[int, str]]:
    enabled: list[tuple[int, str]] = []
    with path.open(encoding="utf-8-sig") as profile:
        for line_number, line in enumerate(profile, 1):
            line = line.rstrip("\r\n")
            if line.startswith("+"):
                enabled.append((line_number, line[1:]))
    return enabled


def _node_attributes(node: ET.Element) -> dict[str, str]:
    result: dict[str, str] = {}
    for attribute in node.findall("./attribute"):
        key = attribute.get("id")
        value = attribute.get("value")
        if key and value is not None:
            result[key] = value
    return result


def parse_modsettings(path: Path) -> tuple[list[str], dict[str, dict[str, str]]]:
    root = ET.parse(path).getroot()
    order: list[str] = []
    metadata: dict[str, dict[str, str]] = {}

    for node in root.iter("node"):
        if node.get("id") == "ModOrder":
            for module in node.findall("./children"):
                uuid = _node_attributes(module).get("UUID")
                if uuid:
                    order.append(uuid)
        elif node.get("id") == "Mods":
            for module in node.findall("./children/node"):
                attributes = _node_attributes(module)
                uuid = attributes.get("UUID")
                if uuid:
                    metadata[uuid] = attributes
    return order, metadata


def _modules_from_settings(
    order: list[str],
    metadata: dict[str, dict[str, str]],
    load_order_offset: int = 0,
) -> tuple[dict[str, Module], dict[str, Module]]:
    by_uuid: dict[str, Module] = {}
    by_folder: dict[str, Module] = {}
    positions = {uuid: load_order_offset + index for index, uuid in enumerate(order)}
    for uuid, attributes in metadata.items():
        module = Module(uuid, attributes.get("Name"), attributes.get("Folder"), positions.get(uuid))
        by_uuid[uuid] = module
        if module.folder:
            by_folder[module.folder.casefold()] = module
    return by_uuid, by_folder


def _metadata_modules(pak: Any, by_uuid: dict[str, Module]) -> list[Module]:
    modules: list[Module] = []
    for entry in pak.names():
        if not entry.lower().endswith("/meta.lsx"):
            continue
        try:
            root = ET.fromstring(pak.read(entry))
        except ET.ParseError:
            continue
        for node in root.iter("node"):
            if node.get("id") != "ModuleInfo":
                continue
            attributes = _node_attributes(node)
            uuid = attributes.get("UUID")
            if uuid:
                modules.append(by_uuid.get(uuid, Module(uuid, attributes.get("Name"), attributes.get("Folder"), None)))
    return modules


def _entry_module(entry: str, by_folder: dict[str, Module], pak_modules: list[Module]) -> Module | None:
    parts = entry.split("/")
    if len(parts) >= 2 and parts[0] in {"Public", "Mods"}:
        matched = by_folder.get(parts[1].casefold())
        if matched:
            return matched
    if len(pak_modules) == 1:
        return pak_modules[0]
    return None


def classify_entry(entry: str) -> str:
    lower = entry.lower()
    parts = {part.casefold() for part in entry.split("/")}
    if "/stats/generated/data/" in lower and lower.endswith(".txt"):
        return "stats"
    if ("treasuretable" in lower or "/treasuretables/" in lower) and lower.endswith(".txt"):
        return "stats"
    if parts.intersection(GAMEPLAY_RESOURCE_PARTS_CASEFOLD):
        if lower.endswith(".lsx"):
            return "lsx"
        if lower.endswith((".lsf", ".lsj")):
            return "resource"
    if (lower.startswith("localization/") or "/localization/" in lower) and lower.endswith((".xml", ".loca")):
        return "localization"
    return "indexed"


def _table_fragment(record_type: str) -> str:
    snake = _CAMEL_BOUNDARY.sub("_", record_type).lower()
    snake = _NON_IDENTIFIER.sub("_", snake).strip("_") or "unknown"
    return snake


class Database:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.tables: dict[str, str] = {}
        self._create_metadata_tables()

    def _create_metadata_tables(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            CREATE TABLE mod_load_order (
                id INTEGER PRIMARY KEY,
                source TEXT NOT NULL,
                source_kind TEXT NOT NULL,
                profile_order INTEGER,
                load_order INTEGER,
                archive_priority INTEGER NOT NULL,
                module_uuid TEXT,
                module_name TEXT,
                module_folder TEXT,
                pak_path TEXT
            );
            CREATE INDEX mod_load_order_source ON mod_load_order(source);
            CREATE INDEX mod_load_order_game ON mod_load_order(load_order);
            CREATE TABLE resources (
                id INTEGER PRIMARY KEY,
                source TEXT NOT NULL,
                source_kind TEXT NOT NULL,
                profile_order INTEGER,
                load_order INTEGER,
                archive_priority INTEGER NOT NULL,
                module_uuid TEXT,
                module_name TEXT,
                pak_path TEXT NOT NULL,
                entry_path TEXT NOT NULL,
                compressed_size INTEGER NOT NULL,
                uncompressed_size INTEGER NOT NULL,
                kind TEXT NOT NULL,
                extracted_rows INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL,
                error TEXT
            );
            CREATE INDEX resources_source ON resources(source);
            CREATE INDEX resources_entry ON resources(entry_path);
            CREATE TABLE data_types (
                record_type TEXT PRIMARY KEY,
                table_name TEXT NOT NULL UNIQUE
            );
            """
        )

    def table_for(self, record_type: str) -> str:
        existing = self.tables.get(record_type)
        if existing:
            return existing
        base = f"type_{_table_fragment(record_type)}"
        table = base
        suffix = 2
        occupied = set(self.tables.values())
        while table in occupied:
            table = f"{base}_{suffix}"
            suffix += 1
        quoted = table.replace('"', '""')
        self.connection.execute(
            f'''CREATE TABLE "{quoted}" (
                id INTEGER PRIMARY KEY,
                source TEXT NOT NULL,
                source_kind TEXT NOT NULL,
                load_order INTEGER,
                archive_priority INTEGER NOT NULL,
                module_uuid TEXT,
                module_name TEXT,
                pak_path TEXT NOT NULL,
                entry_path TEXT NOT NULL,
                format TEXT NOT NULL,
                record_name TEXT,
                record_uuid TEXT,
                using_record TEXT,
                data TEXT NOT NULL CHECK(json_valid(data)),
                raw TEXT
            )'''
        )
        self.connection.execute(f'CREATE INDEX "{quoted}_name" ON "{quoted}"(record_name, load_order)')
        self.connection.execute(f'CREATE INDEX "{quoted}_uuid" ON "{quoted}"(record_uuid, load_order)')
        self.connection.execute("INSERT INTO data_types VALUES (?, ?)", (record_type, table))
        self.tables[record_type] = table
        return table

    @staticmethod
    def _record_values(
        origin: Origin,
        entry: str,
        format_name: str,
        record: Record,
    ) -> tuple[Any, ...]:
        module = origin.module
        return (
            origin.source,
            origin.source_kind,
            origin.load_order,
            origin.archive_priority,
            module.uuid if module else None,
            module.name if module else None,
            origin.pak_path,
            entry,
            format_name,
            record.name,
            record.uuid,
            record.using,
            json.dumps(record.data, ensure_ascii=False, separators=(",", ":")),
            record.raw,
        )

    def insert_records(
        self,
        origin: Origin,
        entry: str,
        format_name: str,
        records: Iterable[Record],
    ) -> int:
        grouped: dict[str, list[tuple[Any, ...]]] = {}
        count = 0
        for record in records:
            table = self.table_for(record.record_type).replace('"', '""')
            grouped.setdefault(table, []).append(
                self._record_values(origin, entry, format_name, record)
            )
            count += 1
        for table, values in grouped.items():
            self.connection.executemany(
                f'''INSERT INTO "{table}"
                    (source, source_kind, load_order, archive_priority, module_uuid, module_name,
                     pak_path, entry_path, format, record_name, record_uuid, using_record, data, raw)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                values,
            )
        return count

    def insert_record(self, origin: Origin, entry: str, format_name: str, record: Record) -> None:
        self.insert_records(origin, entry, format_name, (record,))


def _pak_paths(mod_dir: Path) -> list[Path]:
    return sorted(path for path in mod_dir.rglob("*") if path.is_file() and path.suffix.lower() == ".pak")


def _selected_sources(profile_entries: list[tuple[int, str]], requested: set[str] | None) -> list[tuple[int, str]]:
    if not requested:
        return profile_entries
    enabled = {source for _, source in profile_entries}
    missing = requested - enabled
    if missing:
        raise ValueError("requested source is not enabled: " + ", ".join(sorted(missing)))
    return [(order, source) for order, source in profile_entries if source in requested]

def _base_pak_paths(game_data: Path) -> list[Path]:
    paths = []
    for path in game_data.rglob("*.pak"):
        relative = path.relative_to(game_data).as_posix().casefold()
        name = path.name.casefold()
        if (
            name in BASE_GAME_ARCHIVES
            or name.startswith(("patch", "hotfix"))
            or relative == "localization/english.pak"
        ):
            paths.append(path)
    return sorted(paths)


def _base_archive_order(game_data: Path) -> list[tuple[int, Path]]:
    archives = []
    for path in _base_pak_paths(game_data):
        with path.open("rb") as pak_file:
            header = _forge_pak_header.parse(pak_file.read(64))
        archives.append((header.priority, path))
    archives.sort(key=lambda item: (item[0], item[1].name.casefold()))
    return archives


def _insert_load_rows(
    connection: sqlite3.Connection,
    rows: Iterable[tuple[Any, ...]],
) -> None:
    connection.executemany(
        """INSERT INTO mod_load_order
           (source, source_kind, profile_order, load_order, archive_priority,
            module_uuid, module_name, module_folder, pak_path)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        sorted(rows, key=lambda row: (row[3] is None, row[3] or -1, row[8] or "")),
    )


def _extract_pak(job: PakJob) -> ExtractedPak:
    with _forge_pak_reader(job.path) as pak:
        archive_priority = pak.header.priority
        pak_modules = _metadata_modules(pak, job.by_uuid)
        if job.default_load_order is not None:
            pak_modules = [
                Module(module.uuid, module.name, module.folder, job.default_load_order)
                for module in pak_modules
            ]
        local_folders = dict(job.by_folder)
        for module in pak_modules:
            if module.folder:
                local_folders[module.folder.casefold()] = module

        load_rows: set[tuple[Any, ...]] = set()
        for module in pak_modules:
            load_rows.add(
                (
                    job.source,
                    job.source_kind,
                    job.profile_order,
                    module.load_order,
                    archive_priority,
                    module.uuid,
                    module.name,
                    module.folder,
                    job.relative_pak,
                )
            )

        resources = []
        for archive_entry in pak.entries:
            entry = archive_entry.name
            module = _entry_module(entry, local_folders, pak_modules)
            load_order = (
                module.load_order
                if module is not None and module.load_order is not None
                else job.default_load_order
            )
            if module:
                load_rows.add(
                    (
                        job.source,
                        job.source_kind,
                        job.profile_order,
                        load_order,
                        archive_priority,
                        module.uuid,
                        module.name,
                        module.folder,
                        job.relative_pak,
                    )
                )
            origin = Origin(
                job.source,
                job.source_kind,
                job.profile_order,
                load_order,
                archive_priority,
                job.relative_pak,
                module,
            )
            kind = classify_entry(entry)
            records: tuple[Record, ...] = ()
            status = "indexed"
            error = None
            if kind != "indexed":
                try:
                    payload = pak.read(archive_entry)
                    if kind == "stats":
                        parsed = parse_stats(payload.decode("utf-8-sig"))
                    elif kind == "lsx":
                        parsed = parse_lsx(payload, entry)
                    elif kind == "resource":
                        parsed = parse_binary_resource(payload, entry)
                    else:
                        parsed = parse_localization(
                            payload,
                            entry.lower().endswith(".loca"),
                        )
                    records = tuple(parsed)
                    status = "extracted"
                except (ET.ParseError, UnicodeError, ValueError) as exc:
                    status = "error"
                    error = str(exc)
            resources.append(
                ExtractedResource(
                    origin,
                    entry,
                    archive_entry.size_on_disk,
                    archive_entry.uncompressed_size,
                    kind,
                    records,
                    status,
                    error,
                )
            )

    if not load_rows:
        load_rows.add(
            (
                job.source,
                job.source_kind,
                job.profile_order,
                job.default_load_order,
                archive_priority,
                None,
                None,
                None,
                job.relative_pak,
            )
        )
    return ExtractedPak(job, frozenset(load_rows), tuple(resources))


def _store_extracted_pak(
    database: Database,
    connection: sqlite3.Connection,
    extracted: ExtractedPak,
    counts: dict[str, int],
) -> None:
    resource_rows = []
    for resource in extracted.resources:
        record_count = database.insert_records(
            resource.origin,
            resource.entry,
            resource.kind,
            resource.records,
        )
        module = resource.origin.module
        resource_rows.append(
            (
                resource.origin.source,
                resource.origin.source_kind,
                resource.origin.profile_order,
                resource.origin.load_order,
                resource.origin.archive_priority,
                module.uuid if module else None,
                module.name if module else None,
                resource.origin.pak_path,
                resource.entry,
                resource.compressed_size,
                resource.uncompressed_size,
                resource.kind,
                record_count,
                resource.status,
                resource.error,
            )
        )
        counts["records"] += record_count
        counts["errors"] += resource.status == "error"
    connection.executemany(
        """INSERT INTO resources
           (source, source_kind, profile_order, load_order, archive_priority,
            module_uuid, module_name, pak_path, entry_path, compressed_size,
            uncompressed_size, kind, extracted_rows, status, error)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        resource_rows,
    )
    _insert_load_rows(connection, extracted.load_rows)
    counts["resources"] += len(resource_rows)
    counts["paks"] += 1


def _parallel_extract(jobs: Iterable[PakJob], workers: int) -> Iterator[ExtractedPak]:
    if workers < 1:
        raise ValueError("workers must be at least 1")
    iterator = iter(jobs)
    if workers == 1:
        for job in iterator:
            yield _extract_pak(job)
        return

    with ProcessPoolExecutor(max_workers=workers) as executor:
        pending = []
        for _ in range(workers):
            try:
                pending.append(executor.submit(_extract_pak, next(iterator)))
            except StopIteration:
                break
        while pending:
            future = pending.pop(0)
            yield future.result()
            try:
                pending.append(executor.submit(_extract_pak, next(iterator)))
            except StopIteration:
                pass


def compile_database(
    output: Path,
    install_root: Path = DEFAULT_INSTALL_ROOT,
    profile_name: str = DEFAULT_PROFILE,
    sources: Iterable[str] | None = None,
    progress: bool = True,
    game_data: Path = DEFAULT_GAME_DATA,
    workers: int | None = None,
) -> dict[str, int]:
    _require_bg3forge()
    if not game_data.is_dir():
        raise FileNotFoundError(f"BG3 Data directory does not exist: {game_data}")
    workers = workers if workers is not None else min(16, os.cpu_count() or 1)
    if workers < 1:
        raise ValueError("workers must be at least 1")

    profile_root = install_root / "profiles" / profile_name
    profile_entries = parse_profile(profile_root / "modlist.txt")
    selected = _selected_sources(profile_entries, set(sources) if sources else None)
    native_order, metadata = parse_modsettings(profile_root / "modsettings.lsx")
    base_archives = _base_archive_order(game_data)
    by_uuid, by_folder = _modules_from_settings(native_order, metadata, len(base_archives))
    mods_root = install_root / "mods"

    jobs = [
        PakJob(
            pak_path,
            f"Base Game: {pak_path.relative_to(game_data).as_posix()}",
            "base_game",
            None,
            base_order,
            pak_path.relative_to(game_data).as_posix(),
            {},
            {},
        )
        for base_order, (_, pak_path) in enumerate(base_archives)
    ]
    empty_sources = []
    source_count = 0
    for profile_order, source in selected:
        mod_dir = mods_root / source
        if not mod_dir.is_dir():
            continue
        source_count += 1
        pak_paths = _pak_paths(mod_dir)
        if not pak_paths:
            empty_sources.append(
                (source, "mod", profile_order, None, 0, None, None, None, None)
            )
        for pak_path in pak_paths:
            jobs.append(
                PakJob(
                    pak_path,
                    source,
                    "mod",
                    profile_order,
                    None,
                    pak_path.relative_to(mods_root).as_posix(),
                    by_uuid,
                    by_folder,
                )
            )

    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=output.name + ".", suffix=".tmp", dir=output.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    counts = {
        "sources": source_count,
        "base_paks": len(base_archives),
        "workers": workers,
        "paks": 0,
        "resources": 0,
        "records": 0,
        "errors": 0,
    }

    try:
        connection = sqlite3.connect(temporary)
        connection.executescript(
            """
            PRAGMA journal_mode = OFF;
            PRAGMA synchronous = OFF;
            PRAGMA temp_store = MEMORY;
            PRAGMA locking_mode = EXCLUSIVE;
            """
        )
        database = Database(connection)
        connection.execute("PRAGMA user_version = 2")
        connection.executemany(
            "INSERT INTO metadata VALUES (?, ?)",
            [
                ("install_root", str(install_root)),
                ("game_data", str(game_data)),
                ("profile", profile_name),
                ("workers", str(workers)),
                ("scope", "base game plus enabled character-build gameplay records"),
                ("source_semantics", "base-game archive or Mod Organizer mod directory"),
                ("profile_order_semantics", "one-based line number in modlist.txt; null for base game"),
                (
                    "load_order_semantics",
                    "global zero-based order: retail PAK priority/name, then modsettings.lsx; higher values override lower values",
                ),
            ],
        )
        try:
            for index, extracted in enumerate(_parallel_extract(jobs, workers), 1):
                _store_extracted_pak(database, connection, extracted, counts)
                if progress:
                    print(
                        f"[pak {index}/{len(jobs)}] {extracted.job.relative_pak}",
                        file=sys.stderr,
                    )
            if empty_sources:
                _insert_load_rows(connection, empty_sources)
            connection.commit()
        finally:
            connection.close()
        os.replace(temporary, output)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise
    return counts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="SQLite file to create or atomically replace")
    parser.add_argument("--install-root", type=Path, default=DEFAULT_INSTALL_ROOT)
    parser.add_argument("--game-data", type=Path, default=DEFAULT_GAME_DATA)
    parser.add_argument("--profile", default=DEFAULT_PROFILE)
    parser.add_argument("--source", action="append", help="compile only this enabled MO2 source; repeatable")
    parser.add_argument("--workers", type=int, help="parallel PAK processes; default: up to 16")
    parser.add_argument("--quiet", action="store_true", help="suppress per-mod progress")
    arguments = parser.parse_args(argv)
    counts = compile_database(
        arguments.output,
        install_root=arguments.install_root,
        profile_name=arguments.profile,
        sources=arguments.source,
        progress=not arguments.quiet,
        game_data=arguments.game_data,
        workers=arguments.workers,
    )
    summary = (
        f"wrote {arguments.output}: {counts['records']} records from "
        f"{counts['resources']} resources in {counts['paks']} paks "
        f"with {counts['workers']} workers ({counts['base_paks']} base, "
        f"{counts['sources']} mod sources, {counts['errors']} extraction errors)"
    )
    print(summary)
    return 1 if counts["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
