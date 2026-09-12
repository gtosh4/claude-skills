#!/usr/bin/env python3
"""Dependency-free MCP server for structural markdown navigation.

Emits heading trees carrying line ranges, so a caller can read or edit one
section instead of paging a whole file. Ranges are derived on every call and
stamped with a content digest; they are never cached across edits.
"""

from __future__ import annotations

import glob as globmod
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_FILES = 400
MAX_ROWS = 5000
SKIP_DIRS = frozenset(
    {
        ".git",
        ".hg",
        ".svn",
        "node_modules",
        ".venv",
        "venv",
        "target",
        "dist",
        "build",
        "__pycache__",
        ".next",
        ".cache",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "vendor",
        "site-packages",
    }
)

# ATX headings only. Setext is deliberately unsupported: a standalone `---`
# is a horizontal rule or a front-matter delimiter far more often than an
# underline, and treating it as a heading manufactures false sections.
ATX_RE = re.compile(r"^(#{1,6})(?:[ \t]+(.*?))?[ \t]*$")
FENCE_RE = re.compile(r"^([ \t]*)(`{3,}|~{3,})[ \t]*(\S*)")
TASK_RE = re.compile(r"^[ \t]*[-*+][ \t]+\[(.)\][ \t]+")
FM_KEY_RE = re.compile(r"^([A-Za-z_][\w-]*):[ \t]*(.*)$")
FM_ITEM_RE = re.compile(r"^[ \t]+-[ \t]+(.*)$")
WIKI_RE = re.compile(r"\[\[([^\]|#]*?)(?:#([^\]|]*))?(?:\|([^\]]*))?\]\]")
MDLINK_RE = re.compile(
    r"\[[^\]]*\]\([ \t]*(?!https?://|mailto:|data:|#)([^)\s#]+)(?:#([^)\s]*))?[ \t]*\)"
)
# A bare or backticked filename in prose. Corpora that cite by name rather than
# by link - `(*Heading* in `doc.md`)` - have real references that no link regex
# can see, and renaming a doc breaks them exactly as it breaks a link.
MENTION_RE = re.compile(r"[A-Za-z0-9_][\w.-]*\.(?:md|markdown|mdx)\b")
# Masked out before mention scanning. Without these, `[ext](https://x/a.md)`
# and a bare URL both yield a phantom mention of `a.md`.
ANY_LINK_RE = re.compile(r"\[[^\]]*\]\([^)]*\)")
URL_RE = re.compile(r"\b[A-Za-z][\w+.-]*://\S+")
SETEXT_TRAP_RE = re.compile(r"^(?:-{3,}|\*{3,}|_{3,}|={3,})[ \t]*$")
FM_INTEREST = (
    "title",
    "name",
    "type",
    "status",
    "summary",
    "description",
    "tags",
    "aliases",
    "owns",
)


class OutlineError(RuntimeError):
    pass


def _is_table_separator(line: str) -> bool:
    if "-" not in line or "|" not in line:
        return False
    body = line.strip()
    if not body:
        return False
    return all(ch in "|-: \t" for ch in body)


def _split_cells(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return [c.strip() for c in body.split("|")]


def _resolve(raw: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(raw)))


def _walk_markdown(root: Path) -> list[Path]:
    found: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for name in filenames:
            if name.endswith((".md", ".markdown", ".mdx")):
                found.append(Path(dirpath) / name)
    return found


def _collect(paths: Any) -> list[Path]:
    if isinstance(paths, str):
        paths = [paths]
    if not isinstance(paths, list) or not paths:
        raise OutlineError("`path` must be a string or a non-empty array of strings")
    out: list[Path] = []
    seen: set[Path] = set()
    for entry in paths:
        if not isinstance(entry, str) or not entry.strip():
            raise OutlineError("every `path` entry must be a non-empty string")
        target = _resolve(entry)
        if target.is_dir():
            matches = _walk_markdown(target)
        elif target.exists():
            matches = [target]
        else:
            expanded = globmod.glob(str(target), recursive=True)
            matches = [Path(m) for m in expanded if Path(m).is_file()]
            if not matches:
                raise OutlineError(f"No such file, directory, or glob match: {entry}")
        for match in sorted(matches):
            try:
                key = match.resolve()
            except OSError:
                key = match
            if key not in seen:
                seen.add(key)
                out.append(match)
    if not out:
        raise OutlineError("No markdown files matched")
    return out[:MAX_FILES], len(out)


def _read_text(path: Path) -> tuple[str, str]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise OutlineError(f"Cannot read {path}: {exc.strerror or exc}") from None
    if len(raw) > MAX_FILE_BYTES:
        raise OutlineError(f"{path} exceeds the {MAX_FILE_BYTES // (1024 * 1024)}MiB limit")
    digest = hashlib.sha256(raw).hexdigest()[:8].upper()
    return raw.decode("utf-8", "replace"), digest


def _parse_front_matter(lines: list[str]) -> tuple[dict[str, Any], int]:
    """Return (fields, body_start_index). Front matter must open on line 1."""
    if not lines or lines[0].strip() != "---":
        return {}, 0
    end = None
    for i in range(1, min(len(lines), 200)):
        if lines[i].strip() in ("---", "..."):
            end = i
            break
    if end is None:
        return {}, 0
    fields: dict[str, Any] = {}
    key: str | None = None
    for line in lines[1:end]:
        item = FM_ITEM_RE.match(line)
        if item and key:
            fields.setdefault(key, [])
            if isinstance(fields[key], list):
                fields[key].append(_scalar(item.group(1)))
            continue
        match = FM_KEY_RE.match(line)
        if not match:
            continue
        key, rest = match.group(1), match.group(2).strip()
        if not rest:
            fields[key] = []
        elif rest.startswith("[") and rest.endswith("]"):
            inner = rest[1:-1].strip()
            fields[key] = [_scalar(p) for p in _split_inline(inner)] if inner else []
            key = None
        elif rest in ("|", ">", "|-", ">-", "|+", ">+"):
            fields[key] = ""
            key = None
        else:
            fields[key] = _scalar(rest)
            key = None
    # A bare `key:` followed by an indented mapping rather than a `- ` list is a
    # nested object this parser does not model; drop it instead of claiming [].
    for name in [k for k, v in fields.items() if v == []]:
        del fields[name]
    return fields, end + 1


def _split_inline(inner: str) -> list[str]:
    parts, buf, quote = [], [], None
    for ch in inner:
        if quote:
            if ch == quote:
                quote = None
            else:
                buf.append(ch)
        elif ch in "\"'":
            quote = ch
        elif ch == ",":
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    parts.append("".join(buf))
    return [p.strip() for p in parts if p.strip()]


def _scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value.strip()


def _scan_inline(
    line: str,
    lineno: int,
    links: list[dict[str, Any]],
    tasks: list[tuple[int, str]],
) -> None:
    """Collect tasks and every kind of reference on one line."""
    task = TASK_RE.match(line)
    if task:
        tasks.append((lineno, task.group(1)))

    masked = list(line)

    def blank(start: int, end: int) -> None:
        masked[start:end] = " " * (end - start)

    for match in WIKI_RE.finditer(line):
        target = (match.group(1) or "").strip()
        if target:
            links.append({"line": lineno, "target": target, "kind": "wiki"})
        blank(match.start(), match.end())
    for match in MDLINK_RE.finditer(line):
        links.append({"line": lineno, "target": match.group(1).strip(), "kind": "rel"})
        blank(match.start(), match.end())

    # Mentions are matched against the line with every link construct and bare
    # URL blanked out. Otherwise `[combat.md](combat.md)` is also two mentions
    # of its own filename, and `[ext](https://example.com/a.md)` - which is
    # deliberately not a link - becomes a mention of `a.md`.
    for match in ANY_LINK_RE.finditer(line):
        blank(match.start(), match.end())
    for match in URL_RE.finditer(line):
        blank(match.start(), match.end())

    seen: set[str] = set()
    for match in MENTION_RE.finditer("".join(masked)):
        target = match.group(0)
        if target not in seen:
            seen.add(target)
            links.append({"line": lineno, "target": target, "kind": "mention"})


def parse_document(path: Path, *, keep_lines: bool = False) -> dict[str, Any]:
    text, digest = _read_text(path)
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    nlines = len(lines)
    front, body_start = _parse_front_matter(lines)

    headings: list[dict[str, Any]] = []
    fences: list[dict[str, Any]] = []
    tables: list[dict[str, Any]] = []
    tasks: list[tuple[int, str]] = []
    links: list[dict[str, Any]] = []

    fence_char: str | None = None
    fence_len = 0
    fence_open = 0
    fence_lang = ""
    i = body_start
    while i < nlines:
        line = lines[i]
        lineno = i + 1
        fence = FENCE_RE.match(line)
        if fence_char is not None:
            if (
                fence
                and fence.group(2)[0] == fence_char
                and len(fence.group(2)) >= fence_len
                and not fence.group(3)
            ):
                fences.append(
                    {"start": fence_open, "end": lineno, "lang": fence_lang or "text"}
                )
                fence_char = None
            i += 1
            continue
        if fence:
            fence_char = fence.group(2)[0]
            fence_len = len(fence.group(2))
            fence_open = lineno
            fence_lang = fence.group(3).lower()
            i += 1
            continue

        atx = ATX_RE.match(line)
        if atx:
            title = (atx.group(2) or "").strip().rstrip("#").strip()
            headings.append(
                {"line": lineno, "level": len(atx.group(1)), "title": title or "(untitled)"}
            )
            i += 1
            continue

        if (
            _is_table_separator(line)
            and i - 1 >= body_start
            and "|" in lines[i - 1]
            and not SETEXT_TRAP_RE.match(lines[i - 1].strip())
        ):
            header = _split_cells(lines[i - 1])
            j = i + 1
            while j < nlines and "|" in lines[j] and lines[j].strip():
                j += 1
            tables.append(
                {"start": lineno - 1, "end": j, "rows": j - i - 1, "header": header}
            )
            # The scanner jumps the table body so a row of dashes cannot be
            # mistaken for a second separator, but the rows still hold links -
            # an index table is usually where a doc's links all live. Tasks
            # cannot appear here: TASK_RE is line-anchored and a row starts `|`.
            for k in range(i + 1, j):
                _scan_inline(lines[k], k + 1, links, tasks)
            i = j
            continue

        _scan_inline(line, lineno, links, tasks)
        i += 1

    if fence_char is not None:
        fences.append({"start": fence_open, "end": nlines, "lang": fence_lang or "text", "unclosed": True})

    _attach(headings, lines, nlines, fences, tables, tasks, links)
    doc = {
        "path": str(path),
        "digest": digest,
        "lines": nlines,
        "front_matter": front,
        "headings": headings,
        "counts": {
            "headings": len(headings),
            "fences": len(fences),
            "tables": len(tables),
            "tasks": len(tasks),
            "links": len(links),
        },
    }
    if keep_lines:
        # Opt-in so an outline over hundreds of files does not carry every
        # file's text; md_grep is the only caller that needs it.
        doc["text_lines"] = lines
        doc["body_start"] = body_start
        doc["fence_spans"] = [(f["start"], f["end"]) for f in fences]
    return doc


def _owner(headings: list[dict[str, Any]], line: int) -> dict[str, Any] | None:
    found = None
    for head in headings:
        if head["line"] <= line:
            found = head
        else:
            break
    return found


def _attach(
    headings: list[dict[str, Any]],
    lines: list[str],
    nlines: int,
    fences: list[dict[str, Any]],
    tables: list[dict[str, Any]],
    tasks: list[tuple[int, str]],
    links: list[dict[str, Any]],
) -> None:
    for idx, head in enumerate(headings):
        span_end = nlines
        own_end = nlines
        for nxt in headings[idx + 1 :]:
            if nxt["level"] <= head["level"]:
                span_end = nxt["line"] - 1
                break
        if idx + 1 < len(headings):
            own_end = headings[idx + 1]["line"] - 1
        head["end"] = max(span_end, head["line"])
        own = 0
        for k in range(head["line"], min(own_end, nlines)):
            if lines[k].strip():
                own = k + 2 - head["line"] - 1
        head["own"] = own
        head["fences"] = []
        head["tables"] = []
        head["tasks"] = {}
        head["links"] = []

    # Content above the first heading has no owner. Rather than drop it, expose a
    # synthetic preamble row so a leading table or fence is still addressable.
    def owner_for(line: int) -> dict[str, Any]:
        found = _owner(headings, line)
        if found is not None:
            return found
        if not headings or headings[0].get("title") != "(preamble)":
            first = headings[0]["line"] - 1 if headings else nlines
            headings.insert(
                0,
                {
                    "line": 1,
                    "end": max(first, 1),
                    "level": 1,
                    "title": "(preamble)",
                    "own": max(first, 0),
                    "fences": [],
                    "tables": [],
                    "tasks": {},
                    "links": [],
                },
            )
        return headings[0]

    for fence in fences:
        owner_for(fence["start"])["fences"].append(fence)
    for table in tables:
        owner_for(table["start"])["tables"].append(table)
    for line, state in tasks:
        owner = owner_for(line)
        key = state if state.strip() else " "
        owner["tasks"][key] = owner["tasks"].get(key, 0) + 1
    for link in links:
        owner_for(link["line"])["links"].append(link)


def _fm_summary(front: dict[str, Any], limit: int = 160) -> str:
    parts = []
    for key in FM_INTEREST:
        if key not in front:
            continue
        value = front[key]
        if isinstance(value, list):
            if not value:
                continue
            rendered = "[" + ", ".join(str(v) for v in value[:6]) + "]"
        else:
            rendered = str(value)
            if not rendered:
                continue
            if len(rendered) > limit:
                rendered = rendered[: limit - 1] + "…"
        parts.append(f"{key}={rendered}")
    return "  ".join(parts)


def _task_tag(tasks: dict[str, int]) -> str:
    if not tasks:
        return ""
    total = sum(tasks.values())
    done = tasks.get("x", 0) + tasks.get("X", 0)
    other = {k: v for k, v in tasks.items() if k not in ("x", "X", " ")}
    extra = "".join(f" {k}={v}" for k, v in sorted(other.items()))
    return f"  tasks={done}/{total}{extra}"


def render_text(docs: list[dict[str, Any]], include: set[str], depth: int) -> str:
    out: list[str] = []
    rows = 0
    truncated = False
    for doc in docs:
        head = f"{doc['path']}  [{doc['digest']}]  {doc['lines']}L"
        out.append(head)
        summary = _fm_summary(doc["front_matter"])
        if summary:
            out.append(f"      fm  {summary}")
        if not doc["headings"]:
            out.append("      (no headings)")
        for entry in doc["headings"]:
            if entry["level"] > depth:
                continue
            if rows >= MAX_ROWS:
                truncated = True
                break
            rows += 1
            pad = "  " * (entry["level"] - 1)
            marker = "#" * entry["level"]
            out.append(
                f"{entry['line']:>6}-{entry['end']:<6}{pad} {marker} {entry['title']}"
                f"  own={entry['own']}{_task_tag(entry['tasks'])}"
            )
            blocks: list[tuple[int, str]] = []
            if "tables" in include:
                for table in entry["tables"]:
                    cells = " | ".join(c for c in table["header"][:5] if c)
                    blocks.append(
                        (
                            table["start"],
                            f"{table['start']:>6}-{table['end']:<6}{pad}   table {table['rows']}r  {cells}",
                        )
                    )
            if "fences" in include:
                for fence in entry["fences"]:
                    flag = " UNCLOSED" if fence.get("unclosed") else ""
                    blocks.append(
                        (
                            fence["start"],
                            f"{fence['start']:>6}-{fence['end']:<6}{pad}   fence {fence['lang']}{flag}",
                        )
                    )
            out.extend(row for _, row in sorted(blocks))
            if "links" in include and entry["links"]:
                targets = sorted({l["target"] for l in entry["links"]})
                out.append(f"{'':>13}{pad}   links {', '.join(targets[:10])}")
        if truncated:
            break
        out.append("")
    if truncated:
        out.append(f"… row cap {MAX_ROWS} reached; narrow `path` or lower `depth`")
    return "\n".join(out).rstrip() + "\n"


def _prune(doc: dict[str, Any], include: set[str], depth: int) -> dict[str, Any]:
    headings = []
    for entry in doc["headings"]:
        if entry["level"] > depth:
            continue
        row = {
            "line": entry["line"],
            "end": entry["end"],
            "level": entry["level"],
            "title": entry["title"],
            "own": entry["own"],
        }
        if entry["tasks"]:
            row["tasks"] = entry["tasks"]
        if "tables" in include and entry["tables"]:
            row["tables"] = entry["tables"]
        if "fences" in include and entry["fences"]:
            row["fences"] = entry["fences"]
        if "links" in include and entry["links"]:
            row["links"] = sorted({l["target"] for l in entry["links"]})
        headings.append(row)
    return {
        "path": doc["path"],
        "digest": doc["digest"],
        "lines": doc["lines"],
        "front_matter": doc["front_matter"],
        "counts": doc["counts"],
        "headings": headings,
    }


def _subtree(doc: dict[str, Any], section: str) -> dict[str, Any]:
    pattern = re.compile(section, re.I)
    for idx, entry in enumerate(doc["headings"]):
        if pattern.search(entry["title"]):
            kept = [entry]
            for nxt in doc["headings"][idx + 1 :]:
                if nxt["level"] <= entry["level"]:
                    break
                kept.append(nxt)
            clone = dict(doc)
            clone["headings"] = kept
            clone["section"] = {"title": entry["title"], "range": [entry["line"], entry["end"]]}
            return clone
    raise OutlineError(f"No heading in {doc['path']} matches /{section}/")


def _include_set(arguments: dict[str, Any]) -> set[str]:
    raw = arguments.get("include", ["tables", "fences"])
    if isinstance(raw, str):
        raw = [raw]
    if not isinstance(raw, list):
        raise OutlineError("`include` must be an array of strings")
    allowed = {"tables", "fences", "links"}
    chosen = set()
    for item in raw:
        if item not in allowed:
            raise OutlineError(f"`include` accepts {sorted(allowed)}; got {item!r}")
        chosen.add(item)
    return chosen


def tool_outline(arguments: dict[str, Any]) -> dict[str, Any]:
    files, total = _collect(arguments.get("path"))
    include = _include_set(arguments)
    section = arguments.get("section")
    depth = arguments.get("depth")
    if depth is None:
        depth = 6 if len(files) == 1 else 2
    if not isinstance(depth, int) or not 1 <= depth <= 6:
        raise OutlineError("`depth` must be an integer between 1 and 6")
    fmt = arguments.get("format", "text")
    if fmt not in ("text", "json"):
        raise OutlineError("`format` must be 'text' or 'json'")

    docs, errors = [], []
    for path in files:
        try:
            doc = parse_document(path)
            if section:
                doc = _subtree(doc, section)
            docs.append(doc)
        except OutlineError as exc:
            errors.append(str(exc))
    if not docs:
        raise OutlineError("; ".join(errors) or "No markdown files could be parsed")

    result: dict[str, Any] = {"files": len(docs)}
    if total > len(files):
        result["note"] = f"{total} files matched; showing the first {len(files)}"
    if errors:
        result["errors"] = errors
    if fmt == "json":
        result["documents"] = [_prune(d, include, depth) for d in docs]
    else:
        result["outline"] = render_text(docs, include, depth)
    return result


def tool_locate(arguments: dict[str, Any]) -> dict[str, Any]:
    query = arguments.get("query")
    if not isinstance(query, str) or not query.strip():
        raise OutlineError("`query` must be a non-empty string")
    try:
        pattern = re.compile(query, re.I)
    except re.error as exc:
        raise OutlineError(f"`query` is not a valid regex: {exc}") from None
    files, total = _collect(arguments.get("path"))
    limit = arguments.get("limit", 50)
    if not isinstance(limit, int) or not 1 <= limit <= 500:
        raise OutlineError("`limit` must be an integer between 1 and 500")

    hits, lines_out = [], []
    for path in files:
        try:
            doc = parse_document(path)
        except OutlineError:
            continue
        front = doc["front_matter"]
        # Every front-matter field, not a second hardcoded subset. The routing
        # field a corpus actually uses is its own choice - `owns`, `tags`,
        # `component` - and a locate that cannot see it is a locate that cannot
        # answer "which doc covers this topic".
        meta = []
        for value in front.values():
            if isinstance(value, str):
                meta.append(value)
            elif isinstance(value, list):
                meta.extend(str(item) for item in value)
        if any(pattern.search(m) for m in meta):
            hits.append({"path": doc["path"], "match": "front-matter", "digest": doc["digest"]})
            lines_out.append(f"{doc['path']}  [{doc['digest']}]  front-matter  {_fm_summary(front, 80)}")
        for entry in doc["headings"]:
            if pattern.search(entry["title"]):
                hits.append(
                    {
                        "path": doc["path"],
                        "digest": doc["digest"],
                        "range": [entry["line"], entry["end"]],
                        "level": entry["level"],
                        "title": entry["title"],
                        "own": entry["own"],
                    }
                )
                lines_out.append(
                    f"{doc['path']}:{entry['line']}-{entry['end']}  [{doc['digest']}]"
                    f"  {'#' * entry['level']} {entry['title']}  own={entry['own']}"
                )
            if len(hits) >= limit:
                break
        if len(hits) >= limit:
            break

    result: dict[str, Any] = {"query": query, "searched": len(files), "matches": len(hits)}
    if total > len(files):
        result["note"] = f"{total} files matched `path`; searched the first {len(files)}"
    if arguments.get("format") == "json":
        result["results"] = hits
    else:
        result["results"] = "\n".join(lines_out) if lines_out else "(no matches)"
    return result


def tool_grep(arguments: dict[str, Any]) -> dict[str, Any]:
    """Regex over body prose, reporting the enclosing section for every match.

    The gap this fills: plain grep returns a line with no idea which section
    owns it, and md_locate knows sections but only searches headings. Finding a
    claim and finding the thing you can read or edit are the same question.
    """
    query = arguments.get("query")
    if not isinstance(query, str) or not query.strip():
        raise OutlineError("`query` must be a non-empty string")
    try:
        pattern = re.compile(query, re.I)
    except re.error as exc:
        raise OutlineError(f"`query` is not a valid regex: {exc}") from None
    files, total = _collect(arguments.get("path"))
    limit = arguments.get("limit", 50)
    if not isinstance(limit, int) or not 1 <= limit <= 500:
        raise OutlineError("`limit` must be an integer between 1 and 500")
    section = arguments.get("section")
    section_re = None
    if section is not None:
        if not isinstance(section, str) or not section.strip():
            raise OutlineError("`section` must be a non-empty string")
        try:
            section_re = re.compile(section, re.I)
        except re.error as exc:
            raise OutlineError(f"`section` is not a valid regex: {exc}") from None

    hits: list[dict[str, Any]] = []
    lines_out: list[str] = []
    truncated = False
    for path in files:
        if truncated:
            break
        try:
            doc = parse_document(path, keep_lines=True)
        except OutlineError:
            continue
        headings = doc["headings"]
        spans = doc["fence_spans"]
        for idx in range(doc["body_start"], doc["lines"]):
            line = doc["text_lines"][idx]
            lineno = idx + 1
            if not pattern.search(line):
                continue
            owner = _owner(headings, lineno)
            if section_re is not None and (
                owner is None or not section_re.search(owner["title"])
            ):
                continue
            in_code = any(start <= lineno <= end for start, end in spans)
            hit = {
                "path": doc["path"],
                "line": lineno,
                "text": line.strip()[:200],
                "section": owner["title"] if owner else None,
                "section_range": [owner["line"], owner["end"]] if owner else None,
                "digest": doc["digest"],
            }
            if in_code:
                hit["in_code"] = True
            hits.append(hit)
            where = (
                f"{owner['line']}-{owner['end']} {'#' * owner['level']} {owner['title']}"
                if owner
                else "(no section)"
            )
            tag = "  [code]" if in_code else ""
            lines_out.append(f"{doc['path']}:{lineno}  in {where}{tag}\n    {hit['text']}")
            if len(hits) >= limit:
                truncated = True
                break

    result: dict[str, Any] = {"query": query, "searched": len(files), "matches": len(hits)}
    if truncated:
        result["note"] = f"stopped at the limit of {limit} matches"
    elif total > len(files):
        result["note"] = f"{total} files matched `path`; searched the first {len(files)}"
    if arguments.get("format") == "json":
        result["results"] = hits
    else:
        result["results"] = "\n".join(lines_out) if lines_out else "(no matches)"
    return result


def _link_keys(target: str) -> set[str]:
    stem = target.rsplit("/", 1)[-1]
    for suffix in (".md", ".markdown", ".mdx"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
    return {target, stem, stem.lower()}


def tool_backlinks(arguments: dict[str, Any]) -> dict[str, Any]:
    target = arguments.get("target")
    if not isinstance(target, str) or not target.strip():
        raise OutlineError("`target` must be a non-empty string")
    files, total = _collect(arguments.get("path"))
    wanted = _link_keys(target)
    kinds = arguments.get("kinds", ["wiki", "rel", "mention"])
    if not isinstance(kinds, list) or not kinds:
        raise OutlineError("`kinds` must be a non-empty array")
    unknown = [k for k in kinds if k not in ("wiki", "rel", "mention")]
    if unknown:
        raise OutlineError(f"unknown link kind(s): {', '.join(map(str, unknown))}")
    kinds_set = set(kinds)
    try:
        target_real = _resolve(target).resolve()
    except OSError:
        target_real = None

    hits, lines_out = [], []
    for path in files:
        try:
            doc = parse_document(path)
        except OutlineError:
            continue
        try:
            if target_real is not None and path.resolve() == target_real:
                continue
        except OSError:
            pass
        for entry in doc["headings"]:
            for link in entry["links"]:
                if link["kind"] not in kinds_set:
                    continue
                keys = _link_keys(link["target"])
                if keys & wanted or (
                    link["kind"] == "rel"
                    and target_real is not None
                    and (path.parent / link["target"]).resolve(strict=False) == target_real
                ):
                    hits.append(
                        {
                            "path": doc["path"],
                            "line": link["line"],
                            "kind": link["kind"],
                            "target": link["target"],
                            "section": entry["title"],
                            "section_range": [entry["line"], entry["end"]],
                        }
                    )
                    lines_out.append(
                        f"{doc['path']}:{link['line']}  [{link['kind']}]  in "
                        f"{entry['line']}-{entry['end']} {'#' * entry['level']} {entry['title']}"
                    )
    result: dict[str, Any] = {"target": target, "searched": len(files), "matches": len(hits)}
    if total > len(files):
        result["note"] = f"{total} files matched `path`; searched the first {len(files)}"
    if arguments.get("format") == "json":
        result["results"] = hits
    else:
        result["results"] = "\n".join(lines_out) if lines_out else "(no backlinks)"
    return result


TOOLS = [
    {
        "name": "md_outline",
        "description": (
            "Table of contents for markdown files, where every heading carries its line "
            "range. Use this BEFORE reading a markdown file over ~200 lines: the outline "
            "costs a fraction of the file and each row is a ready-to-use line range for a "
            "ranged read or a section edit. `own` is the heading's own body lines excluding "
            "subsections, so own=0 marks a pure container worth skipping. Also reports YAML "
            "front matter, table and fenced-code ranges, and task-list tallies. Accepts a "
            "file, directory, glob, or array; pass a directory with depth=1 or 2 to map a "
            "whole docs tree. Ranges are recomputed per call and stamped with a content "
            "digest - re-run after editing rather than reusing stale ranges."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {
                    "anyOf": [
                        {"type": "string"},
                        {"type": "array", "items": {"type": "string"}, "minItems": 1},
                    ],
                    "description": "File, directory, glob, or array of them.",
                },
                "depth": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 6,
                    "description": "Deepest heading level to show. Defaults to 6 for one file, 2 for many.",
                },
                "section": {
                    "type": "string",
                    "description": "Case-insensitive regex; outline only the matching heading's subtree.",
                },
                "include": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["tables", "fences", "links"]},
                    "description": "Block kinds to list. Defaults to tables and fences.",
                },
                "format": {"type": "string", "enum": ["text", "json"], "default": "text"},
            },
            "required": ["path"],
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": True},
    },
    {
        "name": "md_locate",
        "description": (
            "Find which markdown file and which section matches a regex, returning "
            "path:start-end ranges. Searches heading text plus every front-matter field, "
            "so a corpus that routes topics through its own key - owns, tags, component - "
            "is searchable by that key. Use instead of grep when the goal is to locate a "
            "section to read or edit, because grep returns matching lines without the "
            "enclosing section's extent. To search body prose rather than headings, use "
            "md_grep."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Case-insensitive regex."},
                "path": {
                    "anyOf": [
                        {"type": "string"},
                        {"type": "array", "items": {"type": "string"}, "minItems": 1},
                    ]
                },
                "limit": {"type": "integer", "minimum": 1, "maximum": 500, "default": 50},
                "format": {"type": "string", "enum": ["text", "json"], "default": "text"},
            },
            "required": ["query", "path"],
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": True},
    },
    {
        "name": "md_grep",
        "description": (
            "Search markdown body text with a regex and get back, for every match, the "
            "line AND the enclosing section with its line range. This is the tool for "
            "finding a claim rather than a heading: plain grep returns a line with no "
            "idea which section owns it, and md_locate knows sections but only searches "
            "heading text and front matter. Matches inside fenced code are reported and "
            "tagged rather than hidden. Pass `section` to search within one part of each "
            "document."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Case-insensitive regex."},
                "path": {
                    "anyOf": [
                        {"type": "string"},
                        {"type": "array", "items": {"type": "string"}, "minItems": 1},
                    ],
                    "description": "File, directory, glob, or array of them.",
                },
                "section": {
                    "type": "string",
                    "description": (
                        "Case-insensitive regex on the enclosing heading; only matches "
                        "inside a matching section are returned."
                    ),
                },
                "limit": {"type": "integer", "minimum": 1, "maximum": 500, "default": 50},
                "format": {"type": "string", "enum": ["text", "json"], "default": "text"},
            },
            "required": ["query", "path"],
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": True},
    },
    {
        "name": "md_backlinks",
        "description": (
            "List every markdown reference pointing at a document, reporting the referring "
            "file, the line, and the enclosing section with its line range. Three kinds of "
            "reference are found: Obsidian [[wiki-links]], relative .md links, and bare or "
            "backticked filename mentions in prose - so a corpus that cites by name rather "
            "than by link is covered too. Use before renaming, moving or deleting a doc to "
            "see what breaks, and to find where a topic is discussed from elsewhere."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {
                    "type": "string",
                    "description": "Document path or bare note name that links point at.",
                },
                "path": {
                    "anyOf": [
                        {"type": "string"},
                        {"type": "array", "items": {"type": "string"}, "minItems": 1},
                    ],
                    "description": "Corpus to scan: directory, glob, or array.",
                },
                "format": {"type": "string", "enum": ["text", "json"], "default": "text"},
                "kinds": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["wiki", "rel", "mention"]},
                    "description": (
                        "Reference kinds to report. Defaults to all three; pass "
                        "[\"wiki\", \"rel\"] for links only."
                    ),
                },
            },
            "required": ["target", "path"],
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": True},
    },
]

TOOL_HANDLERS = {
    "md_outline": tool_outline,
    "md_locate": tool_locate,
    "md_grep": tool_grep,
    "md_backlinks": tool_backlinks,
}


def _tool_result(value: dict[str, Any], is_error: bool = False) -> dict[str, Any]:
    text = value.get("outline") or value.get("results")
    if isinstance(text, str):
        meta = {k: v for k, v in value.items() if k not in ("outline", "results")}
        body = json.dumps(meta, ensure_ascii=False) + "\n" + text
    else:
        body = json.dumps(value, indent=2, ensure_ascii=False)
    return {"content": [{"type": "text", "text": body}], "isError": is_error}


def handle_message(message: dict[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    request_id = message.get("id")
    if request_id is None:
        return None
    if method == "initialize":
        params = message.get("params") if isinstance(message.get("params"), dict) else {}
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": params.get("protocolVersion", "2025-06-18"),
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "markdown-outline", "version": "1.0.0"},
            },
        }
    if method == "ping":
        return {"jsonrpc": "2.0", "id": request_id, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": TOOLS}}
    if method == "tools/call":
        params = message.get("params") if isinstance(message.get("params"), dict) else {}
        name = params.get("name")
        arguments = params.get("arguments") if isinstance(params.get("arguments"), dict) else {}
        handler = TOOL_HANDLERS.get(name)
        if handler is None:
            result = _tool_result({"error": f"Unknown tool: {name}"}, True)
        else:
            try:
                result = _tool_result(handler(arguments))
            except OutlineError as exc:
                result = _tool_result({"error": str(exc)}, True)
            except Exception as exc:  # noqa: BLE001 - protocol must not die on one call
                print(f"markdown-outline internal error: {exc}", file=sys.stderr)
                result = _tool_result({"error": "Internal markdown-outline error"}, True)
        return {"jsonrpc": "2.0", "id": request_id, "result": result}
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def main() -> None:
    for raw_line in sys.stdin.buffer:
        try:
            message = json.loads(raw_line)
            if not isinstance(message, dict):
                continue
            response = handle_message(message)
            if response is not None:
                sys.stdout.write(
                    json.dumps(response, separators=(",", ":"), ensure_ascii=False) + "\n"
                )
                sys.stdout.flush()
        except Exception as exc:  # noqa: BLE001
            print(f"markdown-outline ignored malformed MCP input: {exc}", file=sys.stderr)


if __name__ == "__main__":
    main()
