"""An edit should schedule its dependency closure and nothing else.

The risk of incremental execution is the opposite of the risk of a full rebuild: a rebuild is
merely expensive, while a narrow plan that misses a dependency publishes a stale number that reads
exactly like a fresh one. So every test here checks both halves — what got scheduled, and what
correctly did not.
"""
import glob, json, os, shutil, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "skills", "listo-ledger")
sys.path.insert(0, os.path.join(LEDGER, "scripts"))
import seed_index as SI  # noqa: E402
import work_plan as WP  # noqa: E402
import merge_results as MR  # noqa: E402


class Plan(unittest.TestCase):
    """Runs against copied briefs, a copied seeds file and a synthetic inventory."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        self._deps = SI.DEPS
        self.addCleanup(setattr, SI, "DEPS", self._deps)
        SI.DEPS = {stage: [self._copy(p) for p in paths]
                   for stage, paths in self._deps.items()}
        inv = SI.inventory()
        self.cls = sorted(inv)[0]
        self.sub = inv[self.cls][0]
        self.key = f"{self.cls}/{self.sub}"
        self._real_inventory = SI.inventory
        SI.inventory = lambda: {self.cls: [self.sub]}
        self.addCleanup(setattr, SI, "inventory", self._real_inventory)
        self.seeds = self._seeds_file()
        self.bases = self._bases_file()

    def _copy(self, path):
        dst = os.path.join(self.tmp, os.path.basename(path))
        shutil.copyfile(path, dst)
        return dst

    def _seeds_file(self):
        doc = {"seeds": {self.key: {
            "verdict": "candidate",
            "src": SI.digests(self.cls)[self.sub],
            "seed_deps": SI.deps_hash("seed"),
            "builds": {"lockdown": {"chassis": "Testbody",
                                    "split": f"{self.cls.title()} 20",
                                    "peak": 4, "peak_axis": "act", "breadth": 4,
                                    "why": "because",
                                    "score_deps": SI.deps_hash("score"),
                                    "split_deps": SI.deps_hash("split")}}}}}
        path = os.path.join(self.tmp, "seeds.json")
        with open(path, "w") as fh:
            json.dump(doc, fh)
        return path

    def _bases_file(self):
        """A bases file the audit reads as current, so base drift is a separate signal."""
        with open(os.path.join(LEDGER, "assets", "subclass-bases.json")) as fh:
            real = json.load(fh)
        rec = dict(real["bases"][self.key]) if self.key in real["bases"] else None
        if rec is None:
            return os.path.join(self.tmp, "no-such-bases.json")
        rec["src"] = SI.digests(self.cls)[self.sub]
        rec["base_deps"] = SI.deps_hash("base")
        path = os.path.join(self.tmp, "bases.json")
        with open(path, "w") as fh:
            json.dump({"provenance": real.get("provenance", ""), "bases": {self.key: rec},
                       "arrives": {}}, fh)
        return path

    def _touch(self, stage, name):
        (path,) = [p for p in SI.DEPS[stage] if os.path.basename(p) == name]
        with open(path, "a") as fh:
            fh.write("\n<!-- edited by a test -->\n")

    def plan(self):
        return WP.plan(self.seeds, self.bases)

    def test_an_unchanged_tree_schedules_nothing(self):
        p = self.plan()
        for bucket in ("sweep", "bases", "enumerate", "score"):
            self.assertEqual(p[bucket], [], f"{bucket} should be empty")
        self.assertTrue(p["renderer_only"],
                        "no authored work scheduled means this is a rerender, and it should say so")

    def test_a_rubric_change_schedules_scoring_only(self):
        self._touch("score", "axis-rubrics.md")
        p = self.plan()
        self.assertEqual(p["score"], [f"{self.key}:lockdown"])
        self.assertEqual(p["sweep"], [], "the seed judged a subclass, not a rubric")
        self.assertEqual(p["enumerate"], [])
        self.assertFalse(p["renderer_only"])

    def test_a_dip_catalogue_change_schedules_enumeration_only(self):
        self._touch("split", "dip-catalogue.json")
        p = self.plan()
        self.assertEqual(p["enumerate"], [f"{self.key}:lockdown"])
        self.assertEqual(p["score"], [],
                         "a catalogue edit may select a new body; it cannot falsify the old one")
        self.assertEqual(p["sweep"], [])

    def test_a_sweep_brief_change_schedules_the_sweep_only(self):
        self._touch("seed", "sweep-brief.md")
        p = self.plan()
        self.assertEqual(p["sweep"], [self.key])
        self.assertEqual(p["score"], [], "the seed comes first; the rest may be moot once it is redone")
        self.assertEqual(p["enumerate"], [])

    def test_a_renamed_heading_is_stale_one_way_and_unseeded_the_other(self):
        SI.inventory = lambda: {self.cls: ["A Heading That Did Not Exist Before"]}
        p = self.plan()
        self.assertEqual(p["sweep_stale_keys"], [self.key])
        self.assertIn(f"{self.cls}/A Heading That Did Not Exist Before", p["sweep"])

    def test_the_prose_layer_is_only_scheduled_by_the_selection(self):
        p = self.plan()
        self.assertFalse(p["prose"]["recheck"],
                         "with no ledger to diff, no prose work can be claimed")


class Accounting(unittest.TestCase):
    """Every published chassis lands in exactly one bucket, and the buckets sum to the roster."""

    def test_the_live_ledger_is_fully_accounted_for(self):
        # Derived, not named. The published ledger is `ledger-vN.json` and the superseded one is
        # deleted rather than kept, so a hardcoded version breaks on every publish — this test
        # failed the moment v6 was removed.
        found = sorted(glob.glob(os.path.join(LEDGER, "assets", "ledger-v*.json")))
        led = next(p for p in found if not p.endswith("-provenance.json"))
        p = WP.plan(ledger=led)
        with open(led) as fh:
            total = len(json.load(fh)["chassis"])
        seen = (set(p["retained"]) | set(p["unmapped"])
                | {u["chassis"] for u in p["untraceable"]})
        self.assertEqual(len(seen), total,
                         "a chassis in no bucket is a chassis nobody is accounting for")

    def test_an_address_beats_a_proposed_name(self):
        seeds = {"cleric/Tempest": {"verdict": "candidate",
                                    "builds": {"lockdown": {"chassis": "Proposal",
                                                            "split": "Cleric 20"}}}}
        # `naming.py` resolved the proposal to something else, which is the normal case.
        chassis = {"Resolved": {"address": "cleric/Tempest:lockdown"}}
        self.assertEqual(MR.existing_ids(seeds, chassis),
                         {"cleric/Tempest:lockdown": "Resolved"})

    def test_a_record_with_no_address_is_not_guessed_at(self):
        seeds = {"cleric/Tempest": {"verdict": "candidate",
                                    "builds": {"lockdown": {"chassis": "Proposal",
                                                            "split": "Cleric 20"}}}}
        self.assertEqual(MR.existing_ids(seeds, {"Unrelated": {"split": "Cleric 20"}}), {})


if __name__ == "__main__":
    unittest.main()
