"""The searched split has to reach the seeds, and only a split somebody evaluated may.

The split search ranked variants and nothing consumed the ranking: seeds kept the sweep's guess and
`--check` reported every build as never enumerated. This merges a `listo-variant` pass's choices
back in. Its whole job is refusal — a split from neither the search nor the sweep is a body nobody
evaluated, and that is the one error no later stage can catch, because a body that exists scores
like any other.
"""
import json, os, shutil, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "skills", "listo-ledger")
sys.path.insert(0, os.path.join(LEDGER, "scripts"))
import merge_variants as MV  # noqa: E402
import seed_index as SI  # noqa: E402

SEEDS = os.path.join(LEDGER, "assets", "chassis-seeds.json")
KEY = "cleric/Death"


class Merge(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        # Copies, always. The seeds file is a cache key for three stages.
        self.seeds = os.path.join(self.tmp, "chassis-seeds.json")
        shutil.copyfile(SEEDS, self.seeds)
        with open(self.seeds) as fh:
            self.sweep = json.load(fh)["seeds"][KEY]["builds"]
        self.searched = "Cleric 14 / Bard 6 (College of Swords)"
        self.variants = os.path.join(self.tmp, "variants.json")
        with open(self.variants, "w") as fh:
            # Written in the annotated form the search used to emit, so the strip is exercised.
            json.dump({"format": 1, "split_deps": "x", "variants": {
                KEY: [{"split": self.searched + "  [Bard first]", "value": 70.0,
                       "vector": [0] * 10, "meta": {}}]}}, fh)

    def _sel(self, builds, name="v1-cleric.json"):
        path = os.path.join(self.tmp, name)
        with open(path, "w") as fh:
            json.dump({KEY: {"builds": builds}}, fh)
        return path

    def test_a_searched_split_replaces_the_sweep_guess(self):
        p = self._sel({"lockdown": {"chassis": "Cinder", "split": self.searched, "why": "w"}})
        doc, report = MV.merge([p], self.seeds, self.variants)
        self.assertEqual(doc["seeds"][KEY]["builds"]["lockdown"]["split"], self.searched)
        self.assertEqual(report["searched"], 1)
        self.assertEqual(report["kept_sweep"], 0)

    def test_the_level_one_annotation_is_stripped(self):
        """The search emitted `... [Bard first]`, which `check_split` cannot parse."""
        p = self._sel({"lockdown": {"chassis": "Cinder",
                                    "split": self.searched + "  [Bard first]", "why": "w"}})
        doc, _ = MV.merge([p], self.seeds, self.variants)
        got = doc["seeds"][KEY]["builds"]["lockdown"]["split"]
        self.assertEqual(got, self.searched)
        self.assertEqual(sum(SI.check_split(got, "t").values()), 20)

    def test_keeping_the_sweep_split_is_allowed_and_counted(self):
        niche, b = next(iter(self.sweep.items()))
        p = self._sel({niche: {"chassis": b["chassis"], "split": b["split"], "why": "w",
                               "keep_sweep_reason": "the variants all miss the capstone"}})
        _doc, report = MV.merge([p], self.seeds, self.variants)
        self.assertEqual(report["kept_sweep"], 1)

    def test_a_split_from_nowhere_is_refused(self):
        """The guard that matters: a body nobody evaluated scores like one that was."""
        p = self._sel({"lockdown": {"chassis": "Ghost",
                                    "split": "Cleric 12 / Rogue 8", "why": "w"}})
        with self.assertRaises(SI.SeedError) as e:
            MV.merge([p], self.seeds, self.variants)
        self.assertIn("neither the search nor the sweep", str(e.exception))

    def test_an_unknown_niche_is_refused(self):
        p = self._sel({"blaster": {"chassis": "Ghost", "split": self.searched, "why": "w"}})
        with self.assertRaises(SI.SeedError):
            MV.merge([p], self.seeds, self.variants)

    def test_two_files_cannot_both_claim_a_subclass(self):
        a = self._sel({"lockdown": {"chassis": "A", "split": self.searched, "why": "w"}}, "a.json")
        b = self._sel({"lockdown": {"chassis": "B", "split": self.searched, "why": "w"}}, "b.json")
        with self.assertRaises(SI.SeedError):
            MV.merge([a, b], self.seeds, self.variants)

    def test_an_inherited_peak_is_flagged_as_one(self):
        """`peak` is required by the schema and is a number about the sweep's body, not this one."""
        p = self._sel({"lockdown": {"chassis": "Cinder", "split": self.searched, "why": "w"}})
        doc, _ = MV.merge([p], self.seeds, self.variants)
        self.assertTrue(doc["seeds"][KEY]["builds"]["lockdown"]["peak_inherited"])

    def test_a_forced_build_survives_the_merge_with_its_own_name(self):
        forced = os.path.join(self.tmp, "forced.json")
        addr = f"{KEY}:reaction"
        with open(forced, "w") as fh:
            json.dump({"builds": {addr: {
                "chassis": "Pinned", "split": "Cleric 15 (Death) / Monk 3 / Fighter 2",
                "peak": 4, "peak_axis": "ctrl_a", "breadth": 5, "why": "forced"}}}, fh)
        p = self._sel({"lockdown": {"chassis": "Cinder", "split": self.searched, "why": "w"}})
        doc, report = MV.merge([p], self.seeds, self.variants, forced)
        got = doc["seeds"][KEY]["builds"]["reaction"]
        self.assertEqual(got["chassis"], "Pinned", "a hand-picked name must not be resolved away")
        self.assertEqual(report["forced"], [addr])

    def test_the_merged_file_still_loads(self):
        p = self._sel({"lockdown": {"chassis": "Cinder", "split": self.searched, "why": "w"}})
        doc, _ = MV.merge([p], self.seeds, self.variants)
        out = os.path.join(self.tmp, "candidate.json")
        with open(out, "w") as fh:
            json.dump(doc, fh)
        seeds = SI.load(out)
        self.assertEqual(len(seeds), len(json.load(open(SEEDS))["seeds"]))


if __name__ == "__main__":
    unittest.main()
