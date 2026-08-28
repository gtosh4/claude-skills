import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SERVER = Path(__file__).parents[1] / "server.py"
SPEC = importlib.util.spec_from_file_location("artifact_publisher_server", SERVER)
artifact = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(artifact)

SLUG = "71ad335d-0899-475b-acd7-1583d26b09d3"
URL = f"https://claude.ai/code/artifact/{SLUG}"
VERSION = "1787779858-6169"


class ArtifactServerTests(unittest.TestCase):
    def setUp(self):
        artifact._observed.clear()

    def test_access_token_prefers_explicit_environment_override(self):
        with mock.patch.dict(
            artifact.os.environ, {"CLAUDE_ARTIFACTS_ACCESS_TOKEN": "explicit"}, clear=False
        ):
            self.assertEqual(artifact._access_token(), "explicit")

    @mock.patch.object(artifact, "_stored_oauth")
    @mock.patch.object(artifact, "_omp_oauth")
    def test_access_token_uses_unexpired_omp_login(self, omp_oauth, stored_oauth):
        omp_oauth.return_value = {
            "access": "omp-access",
            "expires": artifact.time.time() * 1000 + 60_000,
        }
        with mock.patch.dict(
            artifact.os.environ, {"CLAUDE_ARTIFACTS_ACCESS_TOKEN": ""}, clear=False
        ):
            self.assertEqual(artifact._access_token(), "omp-access")
        stored_oauth.assert_not_called()

    def test_artifact_url_parser_accepts_query_and_rejects_other_hosts(self):
        self.assertEqual(artifact._artifact_slug(URL + "?via=auto_preview"), SLUG)
        with self.assertRaisesRegex(artifact.ArtifactError, "claude.ai"):
            artifact._artifact_slug(f"https://example.com/code/artifact/{SLUG}")
        with self.assertRaisesRegex(artifact.ArtifactError, "<uuid>"):
            artifact._artifact_slug("https://claude.ai/code/artifact/not-a-uuid")

    def test_served_page_unwrap_and_publish_wrapper(self):
        authored = b"<title>Example</title><main>body</main>"
        served = b"<!doctype html><html><head><!-- frame-runtime --></head><body>\n" + authored + b"\n</body></html>"
        self.assertEqual(artifact._unwrap_served_page(served), authored)
        composed = artifact._compose_page(authored.decode())
        self.assertTrue(composed.startswith("<!doctype html><html><head>"))
        self.assertIn(authored.decode(), composed)
        self.assertTrue(composed.endswith("\n</body></html>"))

    def test_initialize_and_tool_catalog(self):
        initialized = artifact.handle_message(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {"protocolVersion": "2025-11-25"},
            }
        )
        self.assertEqual(initialized["result"]["protocolVersion"], "2025-11-25")
        listed = artifact.handle_message({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        self.assertEqual(
            [tool["name"] for tool in listed["result"]["tools"]],
            ["artifact_list", "artifact_read", "artifact_publish"],
        )

    @mock.patch.object(artifact, "_request_json")
    def test_list_filters_scope_and_limit(self, request_json):
        request_json.return_value = (
            200,
            {
                "frames": [
                    {"slug": SLUG, "title": "Mine", "rel": "mine", "updatedAt": "now"},
                    {
                        "slug": "683f6d8f-959e-41c5-9499-4956cf2c7f6d",
                        "title": "Shared",
                        "rel": "shared",
                    },
                ]
            },
        )
        result = artifact.tool_list({"scope": "mine", "limit": 1})
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["artifacts"][0]["title"], "Mine")

    @mock.patch.object(artifact, "_fetch_served")
    @mock.patch.object(artifact, "_boot")
    def test_read_saves_authored_html_and_records_observation(self, boot, fetch):
        boot.return_value = {
            "ver": VERSION,
            "title": "Example",
            "shared": VERSION,
            "assetToken": "secret-not-returned",
            "perm": {"role": "owner"},
        }
        fetch.return_value = (
            b"<!doctype html><html><head><!-- frame-runtime --></head><body>\n"
            b"<title>Example</title><main>live</main>\n</body></html>"
        )
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "live.html"
            result = artifact.tool_read({"url": URL, "output_path": str(output)})
            self.assertEqual(output.read_text(), "<title>Example</title><main>live</main>")
            self.assertEqual(result["version"], VERSION)
            self.assertEqual(artifact._observed[SLUG]["version"], VERSION)
            self.assertNotIn("secret", json.dumps(result))

    @mock.patch.object(artifact, "_read_live")
    @mock.patch.object(artifact, "_boot")
    def test_publish_refuses_until_live_version_was_read(self, boot, read_live):
        boot_data = {
            "ver": VERSION,
            "title": "Example",
            "favicon": "",
            "perm": {"role": "owner"},
        }
        boot.return_value = boot_data
        read_live.return_value = (boot_data, b"<main>live</main>", Path("/tmp/live.html"))
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "next.html"
            source.write_text("<main>next</main>")
            with self.assertRaisesRegex(artifact.ArtifactError, "not observed"):
                artifact.tool_publish({"url": URL, "file_path": str(source)})
        read_live.assert_called_once_with(SLUG)

    @mock.patch.object(artifact, "_request_json")
    @mock.patch.object(artifact, "_boot")
    def test_publish_sends_observed_base_version(self, boot, request_json):
        boot.return_value = {
            "ver": VERSION,
            "title": "Example",
            "favicon": "flake",
            "perm": {"role": "owner"},
        }
        artifact._observed[SLUG] = {"version": VERSION, "sha256": "old", "path": "/tmp/live"}
        request_json.return_value = (
            200,
            {"slug": SLUG, "version": "1787779999-next", "shared": VERSION},
        )
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "next.html"
            source.write_text("<title>Example</title><main>next</main>")
            result = artifact.tool_publish(
                {"url": URL, "file_path": str(source), "label": "test"}
            )
        method, path, payload = request_json.call_args.args
        self.assertEqual((method, path), ("POST", "/api/frame/deploy/direct"))
        self.assertEqual(payload["baseVersion"], VERSION)
        self.assertIn("<main>next</main>", payload["content"])
        self.assertFalse(result["public_share_is_current"])

    @mock.patch.object(artifact, "_request_json")
    @mock.patch.object(artifact, "_boot")
    def test_publish_conflict_discards_observation(self, boot, request_json):
        boot.return_value = {
            "ver": VERSION,
            "title": "Example",
            "favicon": "",
            "perm": {"role": "owner"},
        }
        artifact._observed[SLUG] = {"version": VERSION}
        request_json.side_effect = artifact.ArtifactHttpError(409, {"conflict": True})
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "next.html"
            source.write_text("<main>next</main>")
            with self.assertRaisesRegex(artifact.ArtifactError, "Publish conflict"):
                artifact.tool_publish({"url": URL, "file_path": str(source)})
        self.assertNotIn(SLUG, artifact._observed)


if __name__ == "__main__":
    unittest.main()
