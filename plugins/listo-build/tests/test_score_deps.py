"""A score's cache key must cover the body it was derived from, not just the rules.

The seed's `src` was the closest thing the pipeline had, and it covers one subclass plus its
class's at-a-glance block. A two- or three-class body reads more than that, so editing the
secondary class used to leave a plausible, current-looking, stale score behind.
"""
import json, os, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "skills", "listo-ledger")
sys.path.insert(0, os.path.join(LEDGER, "scripts"))
import score_deps as SD  # noqa: E402
import seed_index as SI  # noqa: E402

SPLIT = "Cleric 14 (Tempest) / Sorcerer 6 (Storm Sorcery)"
ADDR = "cleric/Tempest:lockdown"


class Sources(unittest.TestCase):

    def setUp(self):
        self.inv = SI.inventory()

    def test_both_classes_contribute(self):
        src, unresolved = SD.body_sources(SPLIT, self.inv)
        self.assertEqual(unresolved, [])
        self.assertIn("cleric.md#at-a-glance", src)
        self.assertIn("cleric.md#Tempest", src)
        # The secondary class is the whole point: the seed's `src` never saw it.
        self.assertIn("sorcerer.md#at-a-glance", src)
        self.assertIn("sorcerer.md#Storm Sorcery (vanilla)", src)

    def test_secondary_class_edit_makes_the_result_stale(self):
        """Fake an edit to the *secondary* class's subclass block."""
        before = SD.deps_for(ADDR, SPLIT, inv=self.inv)["deps"]
        real = SI.sections

        def edited(cls):
            glance, blocks = real(cls)
            if cls == "sorcerer":
                blocks = dict(blocks)
                blocks["Storm Sorcery (vanilla)"] += "\n- a feature that did not use to be here\n"
            return glance, blocks

        SI.sections = edited
        self.addCleanup(setattr, SI, "sections", real)
        after = SD.deps_for(ADDR, SPLIT, inv=self.inv)["deps"]
        self.assertEqual(SD.stale(before, after),
                         ["body_sources:sorcerer.md#Storm Sorcery (vanilla)"])

    def test_unrelated_class_edit_does_not(self):
        real = SI.sections

        def edited(cls):
            glance, blocks = real(cls)
            if cls == "wizard":
                glance += "\nsomething about wizards\n"
            return glance, blocks

        before = SD.deps_for(ADDR, SPLIT, inv=self.inv)["deps"]
        SI.sections = edited
        self.addCleanup(setattr, SI, "sections", real)
        self.assertEqual(SD.stale(before, SD.deps_for(ADDR, SPLIT, inv=self.inv)["deps"]), [])

    def test_schema_edit_is_a_scoring_dependency_and_not_a_sweep_one(self):
        before = SD.deps_for(ADDR, SPLIT, inv=self.inv)["deps"]
        after = dict(before, schema="0" * 12)
        self.assertEqual(SD.stale(before, after), ["schema"])
        # The evidence contract governs what a score must contain. It governs nothing the sweep
        # judged, so it must not appear in any stage that would schedule a re-seed.
        for stage, paths in SI.DEPS.items():
            self.assertNotIn(SD.SCHEMA, paths, f"ledger-schema.md must not be a {stage} dep")

    def test_compiled_data_covers_only_the_classes_involved(self):
        got = SD.compiled_data(SPLIT)
        self.assertEqual(sorted(got), ["listo-10.2-spells.md:cleric",
                                       "listo-10.2-spells.md:sorcerer"])

    def test_pak_evidence_is_recorded_and_compared(self):
        base = SD.deps_for(ADDR, SPLIT, inv=self.inv)["deps"]
        with_pak = SD.deps_for(ADDR, SPLIT, pak_evidence=["Snowlight/Glaring Frost"],
                               inv=self.inv)["deps"]
        self.assertEqual(SD.stale(base, with_pak), ["pak_evidence"])


class Resolution(unittest.TestCase):
    """A split writes the display name; a class file writes the heading."""

    def setUp(self):
        self.inv = SI.inventory()

    def test_display_names_resolve(self):
        for cls, display, want in (
                ("cleric", "Tempest", "Tempest"),
                ("cleric", "Zeal Domain", "Zeal (Hazoret)"),
                ("wizard", "School of Divination", "Divination"),
                ("barbarian", "Zealot", "Path of the Zealot"),
                ("barbarian", "Wildheart", "Base game (Patch 8) — Wildheart"),
                ("mesmerist", "Trickster", "Aspect of the Trickster — the support/buff archetype"),
                ("bard", "College of Lore", "College of Lore (vanilla)")):
            self.assertEqual(SD.resolve_subclass(cls, display, self.inv), want, display)

    def test_a_removed_subclass_fails_closed(self):
        """`Divine Soul` and `The Undead` are documented as removed from the modlist."""
        self.assertIsNone(SD.resolve_subclass("sorcerer", "Divine Soul", self.inv))
        with self.assertRaises(SD.DepsError):
            SD.deps_for("x:y", "Sorcerer 6 (Divine Soul) / Fighter 14 (Battle Master)",
                        inv=self.inv)

    def test_level_one_dip_carries_no_subclass(self):
        parts = SD.split_parts("Fighter 1 (none) / Cleric 14 (Death) / Bard 5 (College of Lore)")
        self.assertEqual([(c, n, s) for c, n, s in parts],
                         [("fighter", 1, None), ("cleric", 14, "Death"),
                          ("bard", 5, "College of Lore")])


class Provenance(unittest.TestCase):
    """Selection provenance is recorded apart from the score's own dependencies."""

    def test_it_is_not_part_of_deps(self):
        doc = SD.deps_for(ADDR, SPLIT)
        self.assertNotIn("selection_provenance", doc["deps"])
        prov = doc["selection_provenance"]
        self.assertIn("cleric/Tempest", prov["subclass_base"])
        self.assertTrue(any(p.startswith("cleric/") for p in prov["dip_parts"]))

    def test_a_moved_base_profile_does_not_make_the_score_stale(self):
        """`stale()` reads `deps` only — that is what keeps a catalogue edit off the score."""
        doc = SD.deps_for(ADDR, SPLIT)
        moved = json.loads(json.dumps(doc))
        moved["selection_provenance"]["subclass_base"]["cleric/Tempest"] = "0" * 12
        self.assertEqual(SD.stale(doc["deps"], moved["deps"]), [])


class LedgerAudit(unittest.TestCase):

    def test_it_names_untraceable_chassis(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "ledger.json")
            with open(path, "w") as fh:
                json.dump({"chassis": {
                    "Good": {"split": SPLIT},
                    "Gone": {"split": "Warlock 3 (The Undead) / Fighter 17 (Battle Master)"}}}, fh)
            total, bad = SD.audit_ledger(path)
        self.assertEqual(total, 2)
        self.assertEqual([cid for cid, _s, _w in bad], ["Gone"])


if __name__ == "__main__":
    unittest.main()
