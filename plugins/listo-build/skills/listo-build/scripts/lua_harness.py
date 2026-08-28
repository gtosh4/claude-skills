"""Run a mod's Script Extender Lua in a sandbox and record what it mutates.

Extracted Stats/LSX records are only half the truth. A Script Extender mod can
rewrite them at runtime through `Ext.StaticData`, and nothing in the extracted
tables shows it -- which makes a negative claim about a runtime grant
unprovable from `type_*` tables alone.

Rather than transcribe each mod's formula by hand, this module executes the
mod's own scripts against a stubbed `Ext` API and records every write it makes
to a static-data object. The effective value therefore stays *evidence* instead
of becoming a transcription that silently rots when the mod updates.

Two deliberate design choices keep this honest:

- Every `Ext` surface we do not implement resolves to a permissive mock that
  records the access path. A mod leaning on an unimplemented API still runs, and
  the paths it wanted are reported in `missing_api` so the gap is visible.
- Nothing is written anywhere. `Ext.IO.SaveFile` is captured, not performed.
"""

from __future__ import annotations

import json
import re
import signal
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Protocol

try:
    import lupa.lua54 as _lupa
except ImportError:  # pragma: no cover - probed by the caller
    try:
        import lupa as _lupa  # type: ignore[no-redef]
    except ImportError:
        _lupa = None

# Ceilings that keep one badly-behaved mod from taking the whole build down.
# These are per sandbox, so exceeding one fails that mod and nothing else.
# Measured need: a spell-list framework walking every record reached ~6.7 GB
# and 38 s on its own, for 7 writes.
MAX_LUA_MEMORY = 512 * 1024 * 1024
MAX_RUNTIME_SECONDS = 60
MAX_RECORD_CACHE = 20000
MAX_MUTATIONS = 250000
MAX_MISSING_API = 2000


class _Deadline(Exception):
    """Raised when one sandbox outstays MAX_RUNTIME_SECONDS."""


_MEMORY_ERRORS: tuple[type[BaseException], ...] = tuple(
    error
    for error in (getattr(_lupa, "LuaMemoryError", None) if _lupa else None, MemoryError)
    if error is not None
)
# Breaching a ceiling must abort the sandbox, so these are re-raised past the
# per-handler `except Exception` that tolerates ordinary mod errors.
_FATAL_ERRORS: tuple[type[BaseException], ...] = (_Deadline, *_MEMORY_ERRORS)


@contextmanager
def _deadline(seconds: int) -> Iterator[None]:
    """Bound wall-clock time for one sandbox.

    Signal timers are main-thread only. Off the main thread the sandbox runs
    untimed -- memory is still capped -- which is stated here rather than
    silently assumed.
    """
    if seconds <= 0 or threading.current_thread() is not threading.main_thread():
        yield
        return

    def _expire(_signum: int, _frame: Any) -> None:
        raise _Deadline()

    previous = signal.signal(signal.SIGALRM, _expire)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)


# Lifecycle events fired after load, in the order the game raises them. A mod
# that mutates progressions subscribes to one of these; firing all of them in
# order is what makes the harness generic.
LIFECYCLE_EVENTS = (
    "ModuleLoadStarted",
    "StatsLoaded",
    "SessionLoading",
    "SessionLoaded",
    "ResetCompleted",
)

_LUA_PRELUDE = """
local record_access, record_write, make_event = ...

local automock

local function mock_index(path)
    return function(_, key)
        local child = path .. "." .. tostring(key)
        record_access(child)
        return automock(child)
    end
end

-- Concatenating a mock must not abort the run: mods build log strings out of
-- metadata we do not model, e.g. `"x" .. Ext.Mod.GetMod(id).Info.ModName`.
local function mock_concat(left, right)
    local function text(value)
        if type(value) == "table" then return "" end
        return tostring(value)
    end
    return text(left) .. text(right)
end

-- Mocks are memoised by path. Allocating a fresh table per access made a mod
-- looping over an unimplemented API allocate without bound (measured: 33 GB
-- peak, build killed). Calling a mock also yields the *same* path rather than
-- appending "()", so a chained call cannot grow the key for ever.
local mock_cache = {}

automock = function(path)
    local existing = mock_cache[path]
    if existing ~= nil then
        return existing
    end
    local created = setmetatable({}, {
        __index = mock_index(path),
        __call = function(_, ...) return automock(path) end,
        __newindex = function() end,
        __tostring = function() return "<mock:" .. path .. ">" end,
        __concat = mock_concat,
        __len = function() return 0 end,
        __pairs = function(t) return function() return nil end, t, nil end,
    })
    mock_cache[path] = created
    return created
end

-- A static-data object. Reads fall through to the real record; writes are
-- recorded before being applied, which is the whole point of the harness.
local function static_proxy(type_name, uuid, backing)
    return setmetatable({}, {
        __index = backing,
        __newindex = function(_, key, value)
            record_write(type_name, uuid, tostring(key), value)
            backing[key] = value
        end,
        __pairs = function() return next, backing, nil end,
        __len = function() return #backing end,
    })
end

-- Any name we do not model resolves to a mock, so one unimplemented API cannot
-- abort a whole mod. Every such name is recorded and reported as `missing_api`,
-- which keeps the gap auditable instead of silent.
local function install_fallback(target, prefix)
    setmetatable(target, {
        __index = function(_, key)
            local path = prefix .. "." .. tostring(key)
            record_access(path)
            return automock(path)
        end,
    })
    return target
end

-- `Ext.Events.<Anything>` must exist before a mod can subscribe to it, and the
-- set of event names is not knowable in advance, so they are created on demand.
local function events_table()
    local cache = {}
    return setmetatable({}, {
        __index = function(_, key)
            local name = tostring(key)
            if cache[name] == nil then
                cache[name] = make_event(name)
            end
            return cache[name]
        end,
    })
end

return automock, static_proxy, install_fallback, events_table
"""

_SAFE_GLOBALS = (
    "assert", "error", "ipairs", "next", "pairs", "pcall", "xpcall", "rawequal",
    "rawget", "rawlen", "rawset", "select", "setmetatable", "getmetatable",
    "tonumber", "tostring", "type", "unpack",
    "string", "table", "math", "coroutine", "utf8", "_VERSION",
)


@dataclass(frozen=True)
class Mutation:
    """One recorded write to a static-data object."""

    record_type: str
    uuid: str
    field: str
    value: Any
    record_name: str | None = None
    record_level: int | None = None


@dataclass
class HarnessResult:
    mod_table: str
    status: str
    error: str | None = None
    mutations: tuple[Mutation, ...] = ()
    log: tuple[str, ...] = ()
    missing_api: tuple[str, ...] = ()
    scripts_run: tuple[str, ...] = ()
    events_fired: tuple[str, ...] = ()
    configs_read: tuple[str, ...] = ()
    script_sha256: str | None = None


class StaticDataSource(Protocol):
    """Backing store for `Ext.StaticData`, normally the compiled database."""

    def get_all(self, type_name: str) -> list[str]:
        ...

    def get(self, uuid: str, type_name: str) -> dict[str, Any] | None:
        ...

    def translate(self, handle: str) -> str:
        ...


def available() -> bool:
    return _lupa is not None


def _to_python(value: Any, depth: int = 0) -> Any:
    """Convert a Lua value to plain Python, bounded so cycles cannot hang."""
    if depth > 8:
        return "<depth-limit>"
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    lua_type = getattr(value, "lua_type", None)
    if lua_type is not None and lua_type() == "table":
        items = list(value.items())
        if items and all(isinstance(key, (int, float)) for key, _ in items):
            ordered = sorted(items, key=lambda pair: pair[0])
            if [key for key, _ in ordered] == list(range(1, len(ordered) + 1)):
                return [_to_python(item, depth + 1) for _, item in ordered]
        return {str(key): _to_python(item, depth + 1) for key, item in items}
    return str(value)


class LuaSandbox:
    """Executes one mod's scripts and reports what it changed."""

    def __init__(
        self,
        mod_table: str,
        scripts: dict[str, str],
        configs: dict[str, str],
        static_data: StaticDataSource,
    ) -> None:
        if _lupa is None:
            raise RuntimeError("lupa is not installed; cannot run Script Extender Lua")
        self.mod_table = mod_table
        self.scripts = scripts
        self.configs = configs
        self.static_data = static_data

        self._mutations: list[Mutation] = []
        self._log: list[str] = []
        self._missing: dict[str, None] = {}
        self._configs_read: list[str] = []
        self._scripts_run: list[str] = []
        self._events: dict[str, list[Any]] = {}
        self._loaded: dict[str, Any] = {}
        self._saved: dict[str, str] = {}

        # A bounded Lua state turns a runaway mod into one failed row rather
        # than an out-of-memory kill that loses the whole build.
        self.runtime = _lupa.LuaRuntime(
            unpack_returned_tuples=True,
            register_eval=False,
            max_memory=MAX_LUA_MEMORY,
        )
        (
            self._automock,
            self._static_proxy,
            self._install_fallback,
            self._events_table,
        ) = self.runtime.execute(
            _LUA_PRELUDE, self._record_access, self._record_write, self._make_event
        )
        self._harden()

    # ---- recording hooks -------------------------------------------------

    def _record_access(self, path: str) -> None:
        if len(self._missing) < MAX_MISSING_API:
            self._missing.setdefault(str(path), None)

    def _record_write(self, type_name: str, uuid: str, key: str, value: Any) -> None:
        if len(self._mutations) >= MAX_MUTATIONS:
            raise RuntimeError(
                f"{self.mod_table} exceeded {MAX_MUTATIONS} static-data writes; "
                "aborting this mod rather than exhausting memory"
            )
        record = self.static_data.get(str(uuid), str(type_name)) or {}
        level = record.get("Level")
        self._mutations.append(
            Mutation(
                record_type=str(type_name),
                uuid=str(uuid),
                field=str(key),
                value=_to_python(value),
                record_name=record.get("Name"),
                record_level=level if isinstance(level, int) else None,
            )
        )

    # ---- sandbox construction -------------------------------------------

    def _harden(self) -> None:
        globals_table = self.runtime.globals()
        allowed = set(_SAFE_GLOBALS)
        for name in list(globals_table.keys()):
            if str(name) not in allowed and str(name) != "_G":
                globals_table[name] = None
        # `traceback` must be a real function: mods pass it to xpcall, which
        # rejects a table outright.
        globals_table["debug"] = self._table(
            {
                "traceback": lambda *_: "",
                "getinfo": lambda *_: self.runtime.table(),
            }
        )
        # Mod `print` is captured, not emitted: a sandboxed mod must not write
        # to the compiler's stdout.
        globals_table["print"] = lambda *parts: self._log.append(
            " ".join(str(_to_python(part)) for part in parts)
        )
        extension = self._build_ext()
        self._install_fallback(extension, "Ext")
        globals_table["Ext"] = extension
        # `Mods` is deliberately left undefined so the global fallback mocks it.
        # Defining it as an empty table would make `Mods.BG3MCM.…` a nil index.
        self._install_fallback(globals_table, "_G")

    def _table(self, mapping: dict[str, Any]) -> Any:
        table = self.runtime.table()
        for key, value in mapping.items():
            table[key] = value
        return table

    def _lua_value(self, value: Any, depth: int = 0) -> Any:
        if depth > 12:
            return None
        if isinstance(value, dict):
            table = self.runtime.table()
            for key, item in value.items():
                table[key] = self._lua_value(item, depth + 1)
            return table
        if isinstance(value, (list, tuple)):
            table = self.runtime.table()
            for index, item in enumerate(value, 1):
                table[index] = self._lua_value(item, depth + 1)
            return table
        return value

    def _build_ext(self) -> Any:
        def ext_require(path: str, *rest: Any) -> Any:
            # Ext.Require("Mod/File.lua") and Ext.Require("File.lua") both occur.
            name = str(rest[0]) if rest else str(path)
            return self._run_script(name)

        def io_load(name: str, *_: Any) -> Any:
            key = str(name)
            self._configs_read.append(key)
            return self.configs.get(key)

        def io_save(name: str, content: Any = "", *_: Any) -> None:
            self._saved[str(name)] = str(content)

        def json_parse(text: str, *_: Any) -> Any:
            try:
                return self._lua_value(json.loads(str(text)))
            except (ValueError, TypeError):
                return None

        def json_stringify(value: Any, *_: Any) -> str:
            return json.dumps(_to_python(value), ensure_ascii=False)

        def static_get_all(type_name: str, *_: Any) -> Any:
            return self._lua_value(self.static_data.get_all(str(type_name)))

        def static_get(uuid: str, type_name: str = "", *_: Any) -> Any:
            record = self.static_data.get(str(uuid), str(type_name))
            if record is None:
                return None
            return self._static_proxy(str(type_name), str(uuid), self._lua_value(record))

        def log(*parts: Any) -> None:
            self._log.append(" ".join(str(_to_python(part)) for part in parts))

        def translate(handle: Any, *_: Any) -> str:
            return self.static_data.translate(str(handle))

        return self._table(
            {
                "Require": ext_require,
                "Events": self._events_table(),
                "IO": self._table({"LoadFile": io_load, "SaveFile": io_save}),
                "Json": self._table({"Parse": json_parse, "Stringify": json_stringify}),
                "StaticData": self._table({"GetAll": static_get_all, "Get": static_get}),
                "Log": self._table(
                    {"Print": log, "PrintError": log, "PrintWarning": log}
                ),
                "Loca": self._table({"GetTranslatedString": translate}),
                "RegisterListener": lambda name, fn, *_: self._subscribe(str(name), fn),
                # Static-data mutation is server-side work, so the harness
                # presents itself as the server to reach that code path.
                "IsServer": lambda *_: True,
                "IsClient": lambda *_: False,
            }
        )

    def _make_event(self, name: str) -> Any:
        return self._event_table(str(name))

    def _event_table(self, name: str) -> Any:
        def subscribe(_self: Any, handler: Any = None, *rest: Any) -> None:
            # Called as Ext.Events.X:Subscribe(fn); tolerate the dot form too.
            callback = handler if handler is not None else _self
            self._subscribe(name, callback)

        return self._table({"Subscribe": subscribe, "Unsubscribe": lambda *_: None})

    def _subscribe(self, name: str, handler: Any) -> None:
        if handler is not None:
            self._events.setdefault(name, []).append(handler)

    # ---- execution -------------------------------------------------------

    def _resolve_script(self, name: str) -> str | None:
        wanted = name.replace("\\", "/").casefold()
        if wanted in self.scripts:
            return wanted
        for key in self.scripts:
            if key.casefold().endswith(wanted) or key.casefold().endswith("/" + wanted):
                return key
        return None

    def _run_script(self, name: str) -> Any:
        key = self._resolve_script(str(name))
        if key is None:
            self._record_access(f"Ext.Require({name})")
            return self._automock(f"require:{name}")
        if key in self._loaded:
            return self._loaded[key]
        self._loaded[key] = True
        self._scripts_run.append(key)
        result = self.runtime.execute(self.scripts[key])
        self._loaded[key] = result if result is not None else True
        return self._loaded[key]

    def _fire_events(self, fired: list[str]) -> None:
        # Fire the known lifecycle first, then anything else the mod subscribed
        # to. One failing handler must not discard the mutations already
        # recorded by the others -- but a breached ceiling must still abort.
        extra = [name for name in self._events if name not in LIFECYCLE_EVENTS]
        for name in (*LIFECYCLE_EVENTS, *sorted(extra)):
            for handler in self._events.get(name, ()):
                try:
                    handler(self.runtime.table())
                    fired.append(name)
                except _FATAL_ERRORS:
                    raise
                except Exception as exc:
                    self._log.append(f"[harness] {name} handler failed: {exc}")

    def run(self, entry_points: tuple[str, ...]) -> HarnessResult:
        status = "ran"
        error: str | None = None
        fired: list[str] = []
        with _deadline(MAX_RUNTIME_SECONDS):
            try:
                ran_any = False
                for entry in entry_points:
                    if self._resolve_script(entry) is not None:
                        self._run_script(entry)
                        ran_any = True
                if not ran_any:
                    status = "no_entry"
                else:
                    self._fire_events(fired)
            except _Deadline:
                status = "timeout"
                error = f"exceeded {MAX_RUNTIME_SECONDS}s"
            except _MEMORY_ERRORS as exc:
                status = "memory_limit"
                error = f"{type(exc).__name__}: exceeded {MAX_LUA_MEMORY // (1024 * 1024)} MB"
            except Exception as exc:
                status = "failed"
                error = f"{type(exc).__name__}: {exc}"

        return HarnessResult(
            mod_table=self.mod_table,
            status=status,
            error=error,
            mutations=tuple(self._mutations),
            log=tuple(self._log),
            missing_api=tuple(self._missing),
            scripts_run=tuple(self._scripts_run),
            events_fired=tuple(dict.fromkeys(fired)),
            configs_read=tuple(dict.fromkeys(self._configs_read)),
        )


def _coerce_attribute(attribute: Any) -> Any:
    """Turn one LSX attribute into the value the Script Extender would expose.

    Driven by the attribute's declared `type`, so this stays generic rather
    than carrying per-record special cases.
    """
    if not isinstance(attribute, dict):
        return attribute
    handle = attribute.get("handle")
    if handle:
        # TranslatedString. Mods reach through `.Handle.Handle`.
        return {
            "Handle": {"Handle": handle, "Version": attribute.get("version")},
            "Value": attribute.get("value") or "",
        }
    raw = attribute.get("value")
    if raw is None:
        return None
    declared = str(attribute.get("type") or "").lower()
    if declared == "bool":
        return str(raw).strip().lower() in {"true", "1"}
    if declared.startswith(("uint", "int")):
        try:
            return int(str(raw).strip())
        except ValueError:
            return 0
    if declared in {"float", "double"}:
        try:
            return float(str(raw).strip())
        except ValueError:
            return 0.0
    return str(raw)


# Values the game supplies for absent attributes. Without these a mod reading
# `progression.Level` on a row that has none would abort the whole run.
_TYPE_DEFAULTS: dict[str, dict[str, Any]] = {
    "Progression": {
        "Level": 0,
        "ProgressionType": 0,
        "IsMulticlass": False,
        "AllowImprovement": False,
        "Name": "",
        "TableUUID": "00000000-0000-0000-0000-000000000000",
        "Selectors": "",
        "Boosts": "",
        "PassivesAdded": "",
    },
    "ClassDescription": {
        "Name": "",
        "ParentGuid": "00000000-0000-0000-0000-000000000000",
        "ProgressionTableUUID": "00000000-0000-0000-0000-000000000000",
    },
}


class SqliteStaticData:
    """`Ext.StaticData` backed by the compiled database, load order resolved."""

    def __init__(self, connection: Any) -> None:
        self.connection = connection
        self._tables: dict[str, str] = {}
        for record_type, table in connection.execute(
            "SELECT record_type, table_name FROM data_types"
        ):
            self._tables[str(record_type)] = str(table)
        self._cache: dict[tuple[str, str], dict[str, Any] | None] = {}
        self._all: dict[str, list[str]] = {}

    def _remember(self, key: tuple[str, str], record: dict[str, Any] | None) -> None:
        """Cache with a ceiling.

        A mod that walks every record would otherwise pin the whole database in
        memory, and several mods walking several types in one build is enough to
        be killed. Dropping the cache wholesale on overflow keeps the common case
        -- a tight loop over one record type -- fast without unbounded growth.
        """
        if len(self._cache) >= MAX_RECORD_CACHE:
            self._cache.clear()
        self._cache[key] = record

    def _table(self, type_name: str) -> str | None:
        return self._tables.get(type_name)

    def get_all(self, type_name: str) -> list[str]:
        cached = self._all.get(type_name)
        if cached is not None:
            return cached
        table = self._table(type_name)
        if table is None:
            self._all[type_name] = []
            return []
        quoted = table.replace('"', '""')
        rows = self.connection.execute(
            f'SELECT DISTINCT record_uuid FROM "{quoted}" WHERE record_uuid IS NOT NULL'
        ).fetchall()
        result = [str(row[0]) for row in rows]
        self._all[type_name] = result
        return result

    def get(self, uuid: str, type_name: str) -> dict[str, Any] | None:
        key = (type_name, uuid)
        if key in self._cache:
            return self._cache[key]
        table = self._table(type_name)
        if table is None:
            self._remember(key, None)
            return None
        quoted = table.replace('"', '""')
        row = self.connection.execute(
            f'''SELECT data FROM "{quoted}" WHERE record_uuid = ?
                ORDER BY load_order IS NULL, load_order DESC, id DESC LIMIT 1''',
            (uuid,),
        ).fetchone()
        if row is None:
            self._remember(key, None)
            return None
        payload = json.loads(row[0])
        attributes = payload.get("attributes") or {}
        record = dict(_TYPE_DEFAULTS.get(type_name, {}))
        for name, attribute in attributes.items():
            record[str(name)] = _coerce_attribute(attribute)
        record.setdefault("UUID", uuid)
        self._remember(key, record)
        return record

    def translate(self, handle: str) -> str:
        table = self._table("Localization")
        if table is None:
            return ""
        quoted = table.replace('"', '""')
        row = self.connection.execute(
            f'''SELECT json_extract(data, '$.text') FROM "{quoted}"
                WHERE record_name = ? ORDER BY load_order DESC, id DESC LIMIT 1''',
            (handle.split(";")[0],),
        ).fetchone()
        return str(row[0]) if row and row[0] else ""


ENTRY_POINTS = ("BootstrapServer.lua", "BootstrapClient.lua", "Bootstrap.lua")


def run_mod(
    mod_table: str,
    scripts: dict[str, str],
    configs: dict[str, str],
    static_data: StaticDataSource,
) -> HarnessResult:
    """Execute one mod's Script Extender entry points and report mutations."""
    sandbox = LuaSandbox(mod_table, scripts, configs, static_data)
    return sandbox.run(ENTRY_POINTS)
