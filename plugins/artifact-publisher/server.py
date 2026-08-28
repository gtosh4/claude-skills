#!/usr/bin/env python3
"""Dependency-free MCP server for conflict-safe claude.ai Artifact updates."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

API_ORIGIN = os.environ.get("CLAUDE_ARTIFACTS_API_ORIGIN", "https://api.anthropic.com").rstrip("/")
BETA_HEADER = "oauth-2025-04-20"
CLIENT_VERSION = "2.1.241"
MAX_JSON_BYTES = 4 * 1024 * 1024
MAX_ARTIFACT_BYTES = 16 * 1024 * 1024
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
VERSION_RE = re.compile(r"^[0-9]{1,15}-[A-Za-z0-9_-]{1,64}$")

FRAME_STYLE = (
    "<style>:root{color-scheme:light}body{margin:0;padding:0;"
    "font:14px -apple-system,BlinkMacSystemFont,sans-serif;"
    "background:#faf9f5;color:#141413}img{max-width:100%}</style>"
)
FRAME_PREFIX = (
    "<!doctype html><html><head><meta charset=utf8>"
    '<meta name=viewport content="width=device-width,initial-scale=1">'
    + FRAME_STYLE
    + "</head><body>\n"
)
FRAME_SUFFIX = "\n</body></html>"
BODY_MARKER = b"</head><body>\n"
BODY_SUFFIX = b"\n</body></html>"


class ArtifactError(RuntimeError):
    pass


class ArtifactHttpError(ArtifactError):
    def __init__(self, status: int, body: Any):
        self.status = status
        self.body = body
        super().__init__(f"Artifact API HTTP {status}: {_brief(body)}")


_observed: dict[str, dict[str, Any]] = {}


def _brief(value: Any, limit: int = 500) -> str:
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    return text[:limit]


def _credential_path() -> Path:
    config = os.environ.get("CLAUDE_CONFIG_DIR")
    root = Path(config).expanduser() if config else Path.home() / ".claude"
    return root / ".credentials.json"

def _omp_credential_path() -> Path:
    configured = os.environ.get("PI_CODING_AGENT_DIR")
    root = Path(configured).expanduser() if configured else Path.home() / ".omp" / "agent"
    return root / "agent.db"


def _omp_oauth() -> dict[str, Any] | None:
    path = _omp_credential_path()
    if not path.is_file():
        return None
    try:
        connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        try:
            row = connection.execute(
                "SELECT data FROM auth_credentials "
                "WHERE provider = 'anthropic' AND credential_type = 'oauth' "
                "AND disabled_cause IS NULL ORDER BY updated_at DESC LIMIT 1"
            ).fetchone()
        finally:
            connection.close()
        if row is None:
            return None
        oauth = json.loads(row[0])
    except (OSError, sqlite3.Error, ValueError, TypeError):
        return None
    if not isinstance(oauth, dict) or not isinstance(oauth.get("access"), str):
        return None
    return oauth


def _unexpired(oauth: dict[str, Any], expiry_key: str) -> bool:
    expires = oauth.get(expiry_key)
    try:
        return expires is None or float(expires) > time.time() * 1000
    except (TypeError, ValueError):
        return False



def _stored_oauth() -> dict[str, Any]:
    path = _credential_path()
    try:
        data = json.loads(path.read_text())
        oauth = data["claudeAiOauth"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise ArtifactError(
            f"No usable Claude Code login at {path}. Run `claude auth login`, "
            "or set CLAUDE_ARTIFACTS_ACCESS_TOKEN."
        ) from exc
    if not isinstance(oauth, dict) or not isinstance(oauth.get("accessToken"), str):
        raise ArtifactError(f"Claude Code credentials at {path} contain no access token")
    return oauth


def _access_token() -> str:
    override = os.environ.get("CLAUDE_ARTIFACTS_ACCESS_TOKEN")
    if override:
        return override
    omp_oauth = _omp_oauth()
    if omp_oauth is not None and _unexpired(omp_oauth, "expires"):
        return omp_oauth["access"]
    try:
        oauth = _stored_oauth()
    except ArtifactError:
        if omp_oauth is not None:
            raise ArtifactError("OMP Anthropic OAuth token is expired; run `/login anthropic` in OMP")
        raise
    if not _unexpired(oauth, "expiresAt"):
        try:
            subprocess.run(
                ["claude", "auth", "status"],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=15,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            pass
        oauth = _stored_oauth()
        if not _unexpired(oauth, "expiresAt"):
            raise ArtifactError("Claude OAuth token is expired; run `claude auth login`")
    return oauth["accessToken"]


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {_access_token()}",
        "anthropic-beta": BETA_HEADER,
        "User-Agent": f"claude-code/{CLIENT_VERSION}",
        "X-Frame-CP": "go",
        "X-Frame-Surface": "code",
        "X-Frame-Platform": "cli",
        "X-Frame-Client-Version": CLIENT_VERSION,
    }


def _read_limited(response: Any, limit: int) -> bytes:
    data = response.read(limit + 1)
    if len(data) > limit:
        raise ArtifactError(f"Artifact response exceeds the {limit}-byte safety limit")
    return data


def _decode_error(raw: bytes) -> Any:
    try:
        return json.loads(raw)
    except (ValueError, UnicodeDecodeError):
        return raw[:1000].decode("utf-8", "replace")


def _request_json(method: str, path: str, payload: dict[str, Any] | None = None) -> tuple[int, Any]:
    headers = _headers()
    body = None
    if payload is not None:
        body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode()
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(
        API_ORIGIN + path,
        data=body,
        headers=headers,
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=70) as response:
            raw = _read_limited(response, MAX_JSON_BYTES)
            return response.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as exc:
        raise ArtifactHttpError(exc.code, _decode_error(exc.read(MAX_JSON_BYTES))) from None
    except urllib.error.URLError as exc:
        raise ArtifactError(f"Artifact API request failed: {exc.reason}") from None


def _artifact_slug(url: str) -> str:
    try:
        parsed = urllib.parse.urlparse(url)
    except ValueError as exc:
        raise ArtifactError("Invalid artifact URL") from exc
    if parsed.scheme != "https" or parsed.hostname != "claude.ai":
        raise ArtifactError("Artifact URL must use https://claude.ai")
    match = re.fullmatch(r"/code/artifact/([^/]+)", parsed.path.rstrip("/"))
    if not match or not UUID_RE.fullmatch(match.group(1)):
        raise ArtifactError("Expected a claude.ai/code/artifact/<uuid> URL")
    return match.group(1).lower()


def _artifact_url(slug: str) -> str:
    return f"https://claude.ai/code/artifact/{slug}"


def _boot(slug: str) -> dict[str, Any]:
    _, data = _request_json("GET", f"/api/frame/{slug}?via=model_read")
    if not isinstance(data, dict) or not VERSION_RE.fullmatch(str(data.get("ver", ""))):
        raise ArtifactError("Artifact boot response is incomplete")
    return data


def _fetch_served(slug: str, boot: dict[str, Any]) -> bytes:
    token = boot.get("assetToken")
    if not isinstance(token, str) or not token:
        raise ArtifactError("Artifact content is not readable by this account")
    version = boot["ver"]
    url = (
        f"https://{slug}.frame.claudeusercontent.com/_f/{version}/index.html"
        f"?__frame_t={urllib.parse.quote(token)}"
    )
    request = urllib.request.Request(url, headers={"User-Agent": f"claude-code/{CLIENT_VERSION}"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return _read_limited(response, MAX_ARTIFACT_BYTES)
    except urllib.error.HTTPError as exc:
        raise ArtifactError(f"Artifact content read failed with HTTP {exc.code}") from None
    except urllib.error.URLError as exc:
        raise ArtifactError(f"Artifact content read failed: {exc.reason}") from None


def _unwrap_served_page(page: bytes) -> bytes:
    start = page.find(BODY_MARKER)
    end = page.rfind(BODY_SUFFIX)
    if start < 0 or end < start:
        raise ArtifactError("Could not safely separate the authored HTML from the viewer wrapper")
    return page[start + len(BODY_MARKER) : end]


def _compose_page(author_html: str) -> str:
    if "\x00" in author_html or "\x1b" in author_html:
        raise ArtifactError("Artifact source contains a refused NUL or ESC byte")
    return FRAME_PREFIX + author_html + FRAME_SUFFIX


def _cache_dir() -> Path:
    base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    path = base / "claude-artifact-mcp" / "reads"
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    try:
        path.chmod(0o700)
    except OSError:
        pass
    return path


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def _read_live(slug: str, output_path: str | None = None) -> tuple[dict[str, Any], bytes, Path]:
    boot = _boot(slug)
    author = _unwrap_served_page(_fetch_served(slug, boot))
    path = (
        Path(output_path).expanduser().resolve()
        if output_path
        else _cache_dir() / f"{slug}-{boot['ver']}.html"
    )
    _atomic_write(path, author)
    digest = hashlib.sha256(author).hexdigest()
    _observed[slug] = {"version": boot["ver"], "sha256": digest, "path": str(path)}
    return boot, author, path


def tool_list(arguments: dict[str, Any]) -> dict[str, Any]:
    limit = arguments.get("limit", 20)
    scope = arguments.get("scope", "mine")
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 50:
        raise ArtifactError("limit must be an integer from 1 to 50")
    if scope not in {"mine", "shared", "all"}:
        raise ArtifactError("scope must be mine, shared, or all")
    _, data = _request_json("GET", "/api/frame/frames?limit=200")
    rows = []
    for row in data.get("frames", []) if isinstance(data, dict) else []:
        if not isinstance(row, dict) or row.get("softDeleted") is True:
            continue
        rel = row.get("rel")
        if scope != "all" and rel != scope:
            continue
        slug = row.get("slug")
        if not isinstance(slug, str) or not UUID_RE.fullmatch(slug):
            continue
        rows.append(
            {
                "title": row.get("title") or "Untitled",
                "url": _artifact_url(slug),
                "updated_at": row.get("updatedAt") or row.get("updated_at"),
                **({"relation": rel} if scope != "mine" else {}),
            }
        )
        if len(rows) >= limit:
            break
    return {"artifacts": rows, "count": len(rows), "scope": scope}


def tool_read(arguments: dict[str, Any]) -> dict[str, Any]:
    url = arguments.get("url")
    output_path = arguments.get("output_path")
    if not isinstance(url, str):
        raise ArtifactError("url is required")
    if output_path is not None and not isinstance(output_path, str):
        raise ArtifactError("output_path must be a string")
    slug = _artifact_slug(url)
    boot, author, path = _read_live(slug, output_path)
    permission = boot.get("perm") if isinstance(boot.get("perm"), dict) else {}
    return {
        "title": boot.get("title") or "Untitled",
        "url": _artifact_url(slug),
        "version": boot["ver"],
        "shared_version": boot.get("shared"),
        "role": permission.get("role") or "reader",
        "bytes": len(author),
        "sha256": hashlib.sha256(author).hexdigest(),
        "source_path": str(path),
    }


def tool_publish(arguments: dict[str, Any]) -> dict[str, Any]:
    url = arguments.get("url")
    file_path = arguments.get("file_path")
    if not isinstance(url, str) or not isinstance(file_path, str):
        raise ArtifactError("url and file_path are required")
    slug = _artifact_slug(url)
    source_path = Path(file_path).expanduser().resolve()
    try:
        source = source_path.read_bytes()
    except OSError as exc:
        raise ArtifactError(f"Could not read file_path: {exc}") from exc
    if len(source) > MAX_ARTIFACT_BYTES:
        raise ArtifactError("Artifact source exceeds 16 MiB")
    try:
        author_html = source.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ArtifactError("Artifact source must be UTF-8 text") from exc

    boot = _boot(slug)
    permission = boot.get("perm") if isinstance(boot.get("perm"), dict) else {}
    if permission.get("role") != "owner":
        raise ArtifactError("Only an artifact owned by this Claude account can be updated")
    live_version = boot["ver"]
    observed = _observed.get(slug)
    if observed is None or observed.get("version") != live_version:
        live_boot, live_author, saved_path = _read_live(slug)
        digest = hashlib.sha256(live_author).hexdigest()
        raise ArtifactError(
            "Publish refused before sending content: the live version was not observed in this "
            f"MCP session. Version {live_boot['ver']} ({digest}) was saved to {saved_path}. "
            "Read and merge that file, then call artifact_publish again."
        )

    payload: dict[str, Any] = {
        "slug": slug,
        "title": arguments.get("title") or boot.get("title") or "Untitled",
        "favicon": arguments.get("favicon") or boot.get("favicon") or "",
        "entrypoint": "cli",
        "baseVersion": live_version,
        "content": _compose_page(author_html),
    }
    for key in ("description", "label"):
        value = arguments.get(key)
        if value is not None:
            if not isinstance(value, str):
                raise ArtifactError(f"{key} must be a string")
            payload[key] = value
    try:
        status, result = _request_json("POST", "/api/frame/deploy/direct", payload)
    except ArtifactHttpError as exc:
        if exc.status == 409:
            _observed.pop(slug, None)
            raise ArtifactError(
                "Publish conflict: the live artifact changed after it was read. "
                "Call artifact_read, merge, and retry."
            ) from None
        raise
    if not isinstance(result, dict) or result.get("slug") != slug or not result.get("version"):
        raise ArtifactError("Deploy returned an incomplete or mismatched response")
    _observed[slug] = {
        "version": result["version"],
        "sha256": hashlib.sha256(source).hexdigest(),
        "path": str(source_path),
    }
    shared = result.get("shared")
    return {
        "url": _artifact_url(slug),
        "version": result["version"],
        "shared_version": shared,
        "public_share_is_current": shared == result["version"],
        "bytes": len(source),
        "sha256": hashlib.sha256(source).hexdigest(),
        "warnings": result.get("warnings", []),
        "http_status": status,
    }


TOOLS = [
    {
        "name": "artifact_list",
        "description": "List claude.ai Code artifacts owned by or shared with the authenticated Claude account.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "minimum": 1, "maximum": 50, "default": 20},
                "scope": {"type": "string", "enum": ["mine", "shared", "all"], "default": "mine"},
            },
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": True},
    },
    {
        "name": "artifact_read",
        "description": "Read the complete authored HTML and current version of a claude.ai Code artifact. Required before updating it.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "output_path": {"type": "string", "description": "Optional local path for the authored HTML."},
            },
            "required": ["url"],
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": True},
    },
    {
        "name": "artifact_publish",
        "description": "Update an owned claude.ai Code artifact from a UTF-8 HTML file. Requires artifact_read first and refuses concurrent changes. Does not move the public share pin.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "file_path": {"type": "string"},
                "title": {"type": "string"},
                "favicon": {"type": "string"},
                "description": {"type": "string"},
                "label": {"type": "string"},
            },
            "required": ["url", "file_path"],
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False},
    },
]
TOOL_HANDLERS = {
    "artifact_list": tool_list,
    "artifact_read": tool_read,
    "artifact_publish": tool_publish,
}


def _tool_result(value: dict[str, Any], is_error: bool = False) -> dict[str, Any]:
    return {
        "content": [{"type": "text", "text": json.dumps(value, indent=2, ensure_ascii=False)}],
        "isError": is_error,
    }


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
                "serverInfo": {"name": "artifact-publisher", "version": "1.0.0"},
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
            except ArtifactError as exc:
                result = _tool_result({"error": str(exc)}, True)
            except Exception as exc:
                print(f"artifact-publisher internal error: {exc}", file=sys.stderr)
                result = _tool_result({"error": "Internal artifact-publisher error"}, True)
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
                sys.stdout.write(json.dumps(response, separators=(",", ":"), ensure_ascii=False) + "\n")
                sys.stdout.flush()
        except Exception as exc:
            print(f"artifact-publisher ignored malformed MCP input: {exc}", file=sys.stderr)


if __name__ == "__main__":
    main()
