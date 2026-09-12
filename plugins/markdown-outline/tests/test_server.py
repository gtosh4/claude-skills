import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SERVER = Path(__file__).parents[1] / "server.py"
SPEC = importlib.util.spec_from_file_location("markdown_outline_server", SERVER)
md = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(md)


class Fixture:
    """Writes markdown to a temp dir and parses it."""

    def __init__(self, body: str, name: str = "doc.md"):
        self.dir = tempfile.TemporaryDirectory()
        self.path = Path(self.dir.name) / name
        self.path.write_text(body, encoding="utf-8")

    def parse(self):
        return md.parse_document(self.path)

    def outline(self, **kwargs):
        args = {"path": str(self.path)}
        args.update(kwargs)
        return md.tool_outline(args)

    def close(self):
        self.dir.cleanup()


def titles(doc):
    return [h["title"] for h in doc["headings"]]


def by_title(doc, title):
    return next(h for h in doc["headings"] if h["title"] == title)


class SectionRangeTests(unittest.TestCase):
    """The span/own contract is the whole point of the tool."""

    def test_span_runs_to_next_same_or_higher_heading_and_own_excludes_children(self):
        fx = Fixture(
            "# Top\n"          # 1
            "intro\n"          # 2
            "## A\n"           # 3
            "a body\n"         # 4
            "### A1\n"         # 5
            "nested\n"         # 6
            "## B\n"           # 7
            "b body\n"         # 8
        )
        self.addCleanup(fx.close)
        doc = fx.parse()
        self.assertEqual(titles(doc), ["Top", "A", "A1", "B"])
        self.assertEqual((by_title(doc, "A")["line"], by_title(doc, "A")["end"]), (3, 6))
        self.assertEqual(by_title(doc, "A")["own"], 1, "own must exclude the A1 subsection")
        self.assertEqual(by_title(doc, "A1")["own"], 1)
        self.assertEqual((by_title(doc, "B")["line"], by_title(doc, "B")["end"]), (7, 8))
        self.assertEqual(by_title(doc, "Top")["end"], 8, "last section runs to EOF")

    def test_container_heading_reports_zero_own_lines(self):
        fx = Fixture("# Top\n## Child\nbody\n")
        self.addCleanup(fx.close)
        self.assertEqual(by_title(fx.parse(), "Top")["own"], 0)

    def test_own_ignores_trailing_blank_lines(self):
        fx = Fixture("# Top\nbody\n\n\n\n## Next\nx\n")
        self.addCleanup(fx.close)
        self.assertEqual(by_title(fx.parse(), "Top")["own"], 1)

    def test_deeper_heading_does_not_close_a_shallower_span(self):
        fx = Fixture("## A\n### x\n#### y\n##### z\n## B\n")
        self.addCleanup(fx.close)
        self.assertEqual(by_title(fx.parse(), "A")["end"], 4)


class HeadingRecognitionTests(unittest.TestCase):
    """Traps measured in the real corpora: 887 rule lines, 17 in-fence comments."""

    def test_horizontal_rule_is_not_a_heading(self):
        fx = Fixture("# Real\n\n---\n\ntext\n\n***\n\n___\n")
        self.addCleanup(fx.close)
        self.assertEqual(titles(fx.parse()), ["Real"])

    def test_setext_underline_is_not_a_heading(self):
        fx = Fixture("# Real\n\nLooks like a title\n===\n\nAnother\n---\n")
        self.addCleanup(fx.close)
        self.assertEqual(titles(fx.parse()), ["Real"])

    def test_hashes_inside_a_fence_are_not_headings(self):
        fx = Fixture("# Real\n\n```sh\n# comment\n## deeper comment\n```\n")
        self.addCleanup(fx.close)
        self.assertEqual(titles(fx.parse()), ["Real"])

    def test_tilde_fence_also_suppresses_headings(self):
        fx = Fixture("# Real\n\n~~~\n# comment\n~~~\n\n## After\n")
        self.addCleanup(fx.close)
        self.assertEqual(titles(fx.parse()), ["Real", "After"])

    def test_closing_hashes_are_stripped_from_the_title(self):
        fx = Fixture("## Title here ###\n")
        self.addCleanup(fx.close)
        self.assertEqual(titles(fx.parse()), ["Title here"])

    def test_seven_hashes_is_not_a_heading(self):
        fx = Fixture("# Real\n\n####### nope\n")
        self.addCleanup(fx.close)
        self.assertEqual(titles(fx.parse()), ["Real"])

    def test_hash_without_space_is_not_a_heading(self):
        fx = Fixture("# Real\n\n#hashtag\n")
        self.addCleanup(fx.close)
        self.assertEqual(titles(fx.parse()), ["Real"])

    def test_heading_inside_front_matter_is_ignored(self):
        fx = Fixture("---\ntitle: x\nnote: '# not a heading'\n---\n\n# Real\n")
        self.addCleanup(fx.close)
        self.assertEqual(titles(fx.parse()), ["Real"])


class FenceTests(unittest.TestCase):
    def test_language_is_captured_and_range_covers_both_delimiters(self):
        fx = Fixture("# T\n\n```rust\nfn f() {}\n```\n")
        self.addCleanup(fx.close)
        fence = by_title(fx.parse(), "T")["fences"][0]
        self.assertEqual((fence["start"], fence["end"], fence["lang"]), (3, 5, "rust"))

    def test_list_indented_fence_is_detected(self):
        fx = Fixture("# T\n\n- item\n  ```rust\n  fn f() {}\n  ```\n- next\n")
        self.addCleanup(fx.close)
        self.assertEqual([f["lang"] for f in by_title(fx.parse(), "T")["fences"]], ["rust"])

    def test_unlabelled_fence_reports_text(self):
        fx = Fixture("# T\n\n```\nplain\n```\n")
        self.addCleanup(fx.close)
        self.assertEqual(by_title(fx.parse(), "T")["fences"][0]["lang"], "text")

    def test_unclosed_fence_is_flagged_and_runs_to_eof(self):
        fx = Fixture("# T\n\n```js\nlet x = 1;\n")
        self.addCleanup(fx.close)
        fence = by_title(fx.parse(), "T")["fences"][0]
        self.assertTrue(fence["unclosed"])
        self.assertEqual(fence["end"], 4)

    def test_longer_backtick_run_closes_only_on_equal_or_longer_run(self):
        fx = Fixture("# T\n\n````md\n```\ninner\n```\n````\n\n## After\n")
        self.addCleanup(fx.close)
        doc = fx.parse()
        self.assertEqual(titles(doc), ["T", "After"])
        self.assertEqual(by_title(doc, "T")["fences"][0]["end"], 7)


class TableTests(unittest.TestCase):
    def test_header_row_and_data_row_count(self):
        fx = Fixture("# T\n\n| A | B |\n|---|---|\n| 1 | 2 |\n| 3 | 4 |\n\nafter\n")
        self.addCleanup(fx.close)
        table = by_title(fx.parse(), "T")["tables"][0]
        self.assertEqual(table["header"], ["A", "B"])
        self.assertEqual((table["start"], table["end"], table["rows"]), (3, 6, 2))

    def test_alignment_markers_and_missing_outer_pipes_parse(self):
        fx = Fixture("# T\n\nA | B\n:--- | ---:\n1 | 2\n")
        self.addCleanup(fx.close)
        self.assertEqual(by_title(fx.parse(), "T")["tables"][0]["rows"], 1)

    def test_table_inside_a_fence_is_not_indexed(self):
        fx = Fixture("# T\n\n```\n| A |\n|---|\n```\n")
        self.addCleanup(fx.close)
        self.assertEqual(by_title(fx.parse(), "T")["tables"], [])

    def test_rule_after_a_pipe_bearing_line_is_not_a_table(self):
        fx = Fixture("# T\n\ntext with | a pipe\n\n---\n\nmore\n")
        self.addCleanup(fx.close)
        self.assertEqual(by_title(fx.parse(), "T")["tables"], [])


class TaskTests(unittest.TestCase):
    def test_nonstandard_states_are_preserved_not_coerced(self):
        fx = Fixture("# T\n\n- [x] done\n- [ ] open\n- [~] partial\n- [~] also\n")
        self.addCleanup(fx.close)
        self.assertEqual(by_title(fx.parse(), "T")["tasks"], {"x": 1, " ": 1, "~": 2})

    def test_task_tag_renders_done_over_total_plus_other_states(self):
        self.assertEqual(md._task_tag({"x": 7, " ": 0, "~": 2}), "  tasks=7/9 ~=2")
        self.assertEqual(md._task_tag({}), "")

    def test_tasks_attribute_to_their_own_section(self):
        fx = Fixture("# T\n## A\n- [x] a\n## B\n- [ ] b\n")
        self.addCleanup(fx.close)
        doc = fx.parse()
        self.assertEqual(by_title(doc, "A")["tasks"], {"x": 1})
        self.assertEqual(by_title(doc, "B")["tasks"], {" ": 1})


class FrontMatterTests(unittest.TestCase):
    def test_inline_list_scalar_and_block_list_all_parse(self):
        fx = Fixture(
            "---\n"
            'title: "Quoted Title"\n'
            "type: design\n"
            'tags: ["a", "b"]\n'
            "aliases:\n  - One\n  - Two\n"
            "---\n\n# Body\n"
        )
        self.addCleanup(fx.close)
        front = fx.parse()["front_matter"]
        self.assertEqual(front["title"], "Quoted Title")
        self.assertEqual(front["type"], "design")
        self.assertEqual(front["tags"], ["a", "b"])
        self.assertEqual(front["aliases"], ["One", "Two"])

    def test_nested_mapping_is_dropped_rather_than_claimed_empty(self):
        fx = Fixture("---\ntitle: x\nnested:\n  inner: y\n---\n\n# B\n")
        self.addCleanup(fx.close)
        self.assertNotIn("nested", fx.parse()["front_matter"])

    def test_front_matter_must_open_on_line_one(self):
        fx = Fixture("\n---\ntitle: x\n---\n\n# B\n")
        self.addCleanup(fx.close)
        self.assertEqual(fx.parse()["front_matter"], {})

    def test_unterminated_front_matter_does_not_swallow_the_document(self):
        fx = Fixture("---\ntitle: x\n\n# Real\n")
        self.addCleanup(fx.close)
        doc = fx.parse()
        self.assertEqual(doc["front_matter"], {})
        self.assertEqual(titles(doc), ["Real"])


class LinkTests(unittest.TestCase):
    def test_wiki_and_relative_links_are_captured_and_urls_skipped(self):
        fx = Fixture(
            "# T\n\n"
            "See [[planet-identity]] and [[power#Section|Power]].\n"
            "Also [docs](technical/power.md) and [ext](https://example.com/a.md).\n"
        )
        self.addCleanup(fx.close)
        links = by_title(fx.parse(), "T")["links"]
        targets = sorted(l["target"] for l in links)
        self.assertEqual(targets, ["planet-identity", "power", "technical/power.md"])

    def test_link_keys_match_a_bare_note_name_against_a_path(self):
        self.assertIn("power", md._link_keys("docs/technical/power.md"))
        self.assertIn("power", md._link_keys("power"))


class PreambleTests(unittest.TestCase):
    def test_blocks_above_the_first_heading_are_still_addressable(self):
        fx = Fixture("intro\n\n| A |\n|---|\n| 1 |\n\n# Real\n")
        self.addCleanup(fx.close)
        doc = fx.parse()
        self.assertEqual(titles(doc), ["(preamble)", "Real"])
        self.assertEqual(doc["headings"][0]["tables"][0]["start"], 3)

    def test_no_preamble_row_when_nothing_precedes_the_first_heading(self):
        fx = Fixture("# Real\n\n| A |\n|---|\n| 1 |\n")
        self.addCleanup(fx.close)
        self.assertEqual(titles(fx.parse()), ["Real"])


class OutlineToolTests(unittest.TestCase):
    def test_text_rows_carry_ranges_and_blocks_sort_by_line(self):
        fx = Fixture(
            "# T\n\n```sh\nx\n```\n\n| A | B |\n|---|---|\n| 1 | 2 |\n"
        )
        self.addCleanup(fx.close)
        rows = [r for r in fx.outline()["outline"].splitlines() if "fence" in r or "table" in r]
        self.assertEqual(len(rows), 2)
        self.assertIn("fence sh", rows[0])
        self.assertIn("table", rows[1])

    def test_include_filters_block_kinds(self):
        fx = Fixture("# T\n\n```sh\nx\n```\n\n| A |\n|---|\n| 1 |\n")
        self.addCleanup(fx.close)
        only_tables = fx.outline(include=["tables"])["outline"]
        self.assertIn("table", only_tables)
        self.assertNotIn("fence", only_tables)

    def test_depth_hides_deeper_headings(self):
        fx = Fixture("# A\n## B\n### C\n")
        self.addCleanup(fx.close)
        shallow = fx.outline(depth=2)["outline"]
        self.assertIn("## B", shallow)
        self.assertNotIn("### C", shallow)

    def test_section_returns_only_the_matching_subtree(self):
        fx = Fixture("# Top\n## Alpha\na\n### Alpha1\nb\n## Beta\nc\n")
        self.addCleanup(fx.close)
        out = fx.outline(section="alpha")["outline"]
        self.assertIn("Alpha", out)
        self.assertIn("Alpha1", out)
        self.assertNotIn("Beta", out)

    def test_section_miss_is_an_error_not_an_empty_outline(self):
        fx = Fixture("# Top\n## Alpha\n")
        self.addCleanup(fx.close)
        with self.assertRaises(md.OutlineError):
            fx.outline(section="Gamma")

    def test_digest_changes_when_the_file_changes(self):
        fx = Fixture("# T\nbody\n")
        self.addCleanup(fx.close)
        first = fx.parse()["digest"]
        fx.path.write_text("# T\nbody edited\n", encoding="utf-8")
        self.assertNotEqual(first, fx.parse()["digest"])

    def test_json_format_emits_structured_headings(self):
        fx = Fixture("# T\nbody\n")
        self.addCleanup(fx.close)
        result = fx.outline(format="json")
        self.assertEqual(result["documents"][0]["headings"][0]["title"], "T")

    def test_empty_and_headingless_files_do_not_raise(self):
        for body in ("", "just prose\n"):
            fx = Fixture(body)
            self.addCleanup(fx.close)
            self.assertIn("outline", fx.outline())


class ValidationTests(unittest.TestCase):
    def test_missing_path_is_reported(self):
        with self.assertRaises(md.OutlineError):
            md.tool_outline({"path": "definitely/not/here.md"})

    def test_bad_include_names_the_allowed_set(self):
        fx = Fixture("# T\n")
        self.addCleanup(fx.close)
        with self.assertRaises(md.OutlineError) as ctx:
            fx.outline(include=["bogus"])
        self.assertIn("tables", str(ctx.exception))

    def test_out_of_range_depth_is_rejected(self):
        fx = Fixture("# T\n")
        self.addCleanup(fx.close)
        for bad in (0, 7, "2"):
            with self.assertRaises(md.OutlineError):
                fx.outline(depth=bad)

    def test_invalid_regex_query_is_reported(self):
        with self.assertRaises(md.OutlineError):
            md.tool_locate({"query": "[unclosed", "path": str(SERVER.parent)})

    def test_empty_path_list_is_rejected(self):
        with self.assertRaises(md.OutlineError):
            md.tool_outline({"path": []})


class LocateAndBacklinkTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        root = Path(self.dir.name)
        (root / "power.md").write_text(
            "---\ntitle: Power Systems\ntags: [energy]\n---\n\n# Power\n## Generators\ndetail\n",
            encoding="utf-8",
        )
        (root / "other.md").write_text(
            "# Other\n## Uses power\nSee [[power]] here.\n## Rel\n[link](power.md)\n",
            encoding="utf-8",
        )
        self.root = str(root)

    def test_locate_matches_heading_text_with_a_range(self):
        result = md.tool_locate({"query": "Generators", "path": self.root, "format": "json"})
        hit = result["results"][0]
        self.assertEqual(hit["title"], "Generators")
        self.assertEqual(hit["range"], [7, 8])

    def test_locate_matches_front_matter_tags(self):
        result = md.tool_locate({"query": "energy", "path": self.root, "format": "json"})
        self.assertTrue(any(h.get("match") == "front-matter" for h in result["results"]))

    def test_locate_honours_limit(self):
        result = md.tool_locate({"query": ".", "path": self.root, "limit": 1, "format": "json"})
        self.assertEqual(len(result["results"]), 1)

    def test_backlinks_report_referrer_and_enclosing_section(self):
        result = md.tool_backlinks({"target": "power", "path": self.root, "format": "json"})
        sections = sorted(h["section"] for h in result["results"])
        self.assertEqual(sections, ["Rel", "Uses power"])

    def test_backlinks_exclude_the_target_itself(self):
        target = str(Path(self.dir.name) / "power.md")
        result = md.tool_backlinks({"target": target, "path": self.root, "format": "json"})
        self.assertTrue(all(h["path"] != target for h in result["results"]))

    def test_backlinks_report_no_matches_cleanly(self):
        result = md.tool_backlinks({"target": "nonexistent-note", "path": self.root})
        self.assertEqual(result["matches"], 0)


class ProtocolTests(unittest.TestCase):
    def test_initialize_echoes_protocol_and_names_the_server(self):
        reply = md.handle_message(
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-03-26"}}
        )
        self.assertEqual(reply["result"]["protocolVersion"], "2025-03-26")
        self.assertEqual(reply["result"]["serverInfo"]["name"], "markdown-outline")

    def test_tools_list_exposes_exactly_the_read_only_tools(self):
        tools = md.handle_message({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})["result"]["tools"]
        self.assertEqual(
            sorted(t["name"] for t in tools),
            ["md_backlinks", "md_grep", "md_locate", "md_outline"],
        )
        self.assertTrue(all(t["annotations"]["readOnlyHint"] for t in tools))
        self.assertEqual(sorted(md.TOOL_HANDLERS), sorted(t["name"] for t in tools))

    def test_every_tool_schema_is_closed_and_declares_required_inputs(self):
        for tool in md.TOOLS:
            schema = tool["inputSchema"]
            self.assertFalse(schema["additionalProperties"], tool["name"])
            self.assertIn("path", schema["required"], tool["name"])

    def test_notifications_get_no_response(self):
        self.assertIsNone(md.handle_message({"jsonrpc": "2.0", "method": "notifications/initialized"}))

    def test_unknown_method_returns_method_not_found(self):
        reply = md.handle_message({"jsonrpc": "2.0", "id": 3, "method": "resources/list"})
        self.assertEqual(reply["error"]["code"], -32601)

    def test_unknown_tool_is_an_error_result_not_a_crash(self):
        reply = md.handle_message(
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "md_nope", "arguments": {}}}
        )
        self.assertTrue(reply["result"]["isError"])

    def test_tool_error_is_surfaced_as_an_error_result(self):
        reply = md.handle_message(
            {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "tools/call",
                "params": {"name": "md_outline", "arguments": {"path": "no/such.md"}},
            }
        )
        self.assertTrue(reply["result"]["isError"])
        self.assertIn("No such file", reply["result"]["content"][0]["text"])

    def test_text_results_are_not_json_wrapped_line_noise(self):
        fx = Fixture("# T\nbody\n")
        self.addCleanup(fx.close)
        reply = md.handle_message(
            {
                "jsonrpc": "2.0",
                "id": 6,
                "method": "tools/call",
                "params": {"name": "md_outline", "arguments": {"path": str(fx.path)}},
            }
        )
        text = reply["result"]["content"][0]["text"]
        header, _, body = text.partition("\n")
        self.assertEqual(json.loads(header)["files"], 1)
        self.assertIn("# T", body)


class DirectoryTests(unittest.TestCase):
    def test_skipped_directories_are_not_walked(self):
        root = tempfile.TemporaryDirectory()
        self.addCleanup(root.cleanup)
        base = Path(root.name)
        (base / "keep.md").write_text("# Keep\n", encoding="utf-8")
        junk = base / "node_modules"
        junk.mkdir()
        (junk / "skip.md").write_text("# Skip\n", encoding="utf-8")
        result = md.tool_outline({"path": str(base)})
        self.assertEqual(result["files"], 1)
        self.assertIn("Keep", result["outline"])
        self.assertNotIn("Skip", result["outline"])

    def test_multi_file_default_depth_is_two(self):
        root = tempfile.TemporaryDirectory()
        self.addCleanup(root.cleanup)
        base = Path(root.name)
        for name in ("a.md", "b.md"):
            (base / name).write_text("# H1\n## H2\n### H3\n", encoding="utf-8")
        outline = md.tool_outline({"path": str(base)})["outline"]
        self.assertIn("## H2", outline)
        self.assertNotIn("### H3", outline)

    def test_duplicate_paths_are_deduplicated(self):
        fx = Fixture("# T\n")
        self.addCleanup(fx.close)
        result = md.tool_outline({"path": [str(fx.path), str(fx.path)]})
        self.assertEqual(result["files"], 1)


class TableInteriorTests(unittest.TestCase):
    """An index table is usually where a doc's links all live."""

    def test_links_inside_table_rows_are_captured(self):
        fx = Fixture(
            "# Index\n\n"
            "| Doc | Covers |\n"
            "|---|---|\n"
            "| [combat.md](combat.md) | hits |\n"
            "| [bodies.md](bodies.md) | organs |\n"
        )
        self.addCleanup(fx.close)
        doc = fx.parse()
        targets = sorted(l["target"] for l in by_title(doc, "Index")["links"] if l["kind"] == "rel")
        self.assertEqual(targets, ["bodies.md", "combat.md"])

    def test_the_table_itself_is_still_one_table(self):
        fx = Fixture("# T\n\n| A | B |\n|---|---|\n| - | - |\n| 1 | 2 |\n")
        self.addCleanup(fx.close)
        tables = by_title(fx.parse(), "T")["tables"]
        self.assertEqual(len(tables), 1, "a dash-only row must not read as a second separator")
        self.assertEqual(tables[0]["rows"], 2)


class MentionTests(unittest.TestCase):
    def test_a_backticked_filename_in_prose_is_a_mention(self):
        fx = Fixture("# T\n\nSee (*Hits* in `combat.md`) for the shape.\n")
        self.addCleanup(fx.close)
        links = by_title(fx.parse(), "T")["links"]
        self.assertEqual([(l["kind"], l["target"]) for l in links], [("mention", "combat.md")])

    def test_a_link_is_not_also_counted_as_a_mention_of_itself(self):
        fx = Fixture("# T\n\n[combat.md](combat.md)\n")
        self.addCleanup(fx.close)
        kinds = [l["kind"] for l in by_title(fx.parse(), "T")["links"]]
        self.assertEqual(kinds, ["rel"])

    def test_a_md_inside_an_external_url_is_not_a_mention(self):
        fx = Fixture("# T\n\n[ext](https://example.com/a.md) and https://x.dev/b.md\n")
        self.addCleanup(fx.close)
        self.assertEqual(by_title(fx.parse(), "T")["links"], [])

    def test_backlinks_finds_prose_citations_and_kinds_filters_them_out(self):
        root = tempfile.TemporaryDirectory()
        self.addCleanup(root.cleanup)
        base = Path(root.name)
        (base / "combat.md").write_text("# Combat\n", encoding="utf-8")
        (base / "defence.md").write_text(
            "# Defence\n\n## Answers\n\nTyped threats live in `combat.md`.\n", encoding="utf-8"
        )
        found = md.tool_backlinks({"target": "combat.md", "path": str(base), "format": "json"})
        self.assertEqual(found["matches"], 1)
        hit = found["results"][0]
        self.assertEqual((hit["kind"], hit["section"], hit["section_range"]), ("mention", "Answers", [3, 5]))
        links_only = md.tool_backlinks(
            {"target": "combat.md", "path": str(base), "kinds": ["wiki", "rel"]}
        )
        self.assertEqual(links_only["matches"], 0)

    def test_unknown_link_kind_is_rejected(self):
        with self.assertRaises(md.OutlineError):
            md.tool_backlinks({"target": "x.md", "path": ".", "kinds": ["bogus"]})


class LocateFrontMatterTests(unittest.TestCase):
    def test_any_front_matter_field_is_searchable_not_a_fixed_subset(self):
        fx = Fixture("---\nowns: [organ, organ-schema]\n---\n\n# What an organ is\n")
        self.addCleanup(fx.close)
        found = md.tool_locate({"query": "organ-schema", "path": str(fx.path), "format": "json"})
        self.assertEqual(found["matches"], 1)
        self.assertEqual(found["results"][0]["match"], "front-matter")


class GrepTests(unittest.TestCase):
    def test_a_prose_match_reports_its_enclosing_section_range(self):
        fx = Fixture(
            "# Top\n"           # 1
            "## Recovery\n"     # 2
            "charges refill\n"  # 3
            "## Threat\n"       # 4
            "enmity\n"          # 5
        )
        self.addCleanup(fx.close)
        found = md.tool_grep({"query": "charges", "path": str(fx.path), "format": "json"})
        self.assertEqual(found["matches"], 1)
        hit = found["results"][0]
        self.assertEqual((hit["line"], hit["section"], hit["section_range"]), (3, "Recovery", [2, 3]))

    def test_section_filter_restricts_matches_to_one_part_of_the_doc(self):
        fx = Fixture("# Top\n## A\nneedle\n## B\nneedle\n")
        self.addCleanup(fx.close)
        found = md.tool_grep(
            {"query": "needle", "path": str(fx.path), "section": "^B$", "format": "json"}
        )
        self.assertEqual([h["line"] for h in found["results"]], [5])

    def test_front_matter_is_not_searched_as_body(self):
        fx = Fixture("---\nowns: [needle]\n---\n\n# T\nbody\n")
        self.addCleanup(fx.close)
        self.assertEqual(md.tool_grep({"query": "needle", "path": str(fx.path)})["matches"], 0)

    def test_matches_inside_fenced_code_are_tagged_rather_than_hidden(self):
        fx = Fixture("# T\n\n```rust\nlet needle = 1;\n```\n")
        self.addCleanup(fx.close)
        found = md.tool_grep({"query": "needle", "path": str(fx.path), "format": "json"})
        self.assertEqual(found["matches"], 1)
        self.assertTrue(found["results"][0]["in_code"])

    def test_limit_stops_the_scan_and_says_so(self):
        fx = Fixture("# T\n" + "needle\n" * 10)
        self.addCleanup(fx.close)
        found = md.tool_grep({"query": "needle", "path": str(fx.path), "limit": 3})
        self.assertEqual(found["matches"], 3)
        self.assertIn("limit", found["note"])

    def test_an_invalid_regex_is_an_error_not_a_crash(self):
        with self.assertRaises(md.OutlineError):
            md.tool_grep({"query": "([unclosed", "path": "."})


if __name__ == "__main__":
    unittest.main()
