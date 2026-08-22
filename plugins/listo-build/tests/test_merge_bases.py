"""Base profiles and their grant arrival levels come back from one pass, in two explicit maps.

The grants correction pass existed because the original contract asked for level-1 grants when a
mono-20 body holds everything it ever gains. Fixing that cost a second full-inventory traversal
that re-read the same briefs, the same rubrics and the same class sections as the pass it was
correcting. Fusing them removes the second read; keeping the two maps explicit and separately
validated is what stops them drifting apart again.
"""
import json, os, shutil, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "skills", "listo-ledger")
sys.path.insert(0, os.path.join(LEDGER, "scripts"))
import merge_bases as MB  # noqa: E402
import seed_index as SI  # noqa: E402

PUBLISHED = os.path.join(LEDGER, "assets", "subclass-bases.json")


def published():
    with open(PUBLISHED) as fh:
        return json.load(fh)


class Fused(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        doc = published()
        # A copy, always. The base profiles are a cache key for two stages.
        self.into = os.path.join(self.tmp, "subclass-bases.json")
        shutil.copyfile(PUBLISHED, self.into)
        self.key = next(k for k, v in doc["bases"].items()
                        if v["verdict"] == "candidate" and doc["arrives"].get(k))
        self.rec = {f: v for f, v in doc["bases"][self.key].items()
                    if f not in ("src", "base_deps")}
        self.arr = doc["arrives"][self.key]

    def _write(self, bases, arrives, name="out.json"):
        path = os.path.join(self.tmp, name)
        with open(path, "w") as fh:
            json.dump({"bases": bases, "arrives": arrives}, fh)
        return path

    def test_an_unchanged_pass_round_trips(self):
        path = self._write({self.key: self.rec}, {self.key: self.arr})
        doc, report = MB.merge([path], self.into)
        self.assertEqual(report["unchanged"], [self.key])
        self.assertEqual(doc["arrives"][self.key], self.arr)

    def test_the_cache_stamps_are_carried_not_authored(self):
        """Merging a pass must not mark it current — `--bases --stamp` is that decision."""
        before = published()["bases"][self.key]
        path = self._write({self.key: self.rec}, {self.key: self.arr})
        doc, _ = MB.merge([path], self.into)
        for f in ("src", "base_deps"):
            if f in before:
                self.assertEqual(doc["bases"][self.key][f], before[f])

    def test_a_changed_field_is_named(self):
        rec = dict(self.rec, why="a different justification entirely")
        path = self._write({self.key: rec}, {self.key: self.arr})
        _doc, report = MB.merge([path], self.into)
        self.assertEqual(report["changed"][self.key], ["why"])

    def test_a_missing_arrives_map_is_an_evidence_gap(self):
        path = self._write({self.key: self.rec}, {})
        with self.assertRaises(SI.SeedError) as e:
            MB.merge([path], self.into)
        self.assertIn("arrives", str(e.exception))

    def test_an_empty_arrives_map_is_a_valid_answer(self):
        path = self._write({self.key: self.rec}, {self.key: {}})
        doc, report = MB.merge([path], self.into)
        self.assertNotIn(self.key, doc["arrives"])
        self.assertIn(self.key, report["arrives_changed"])

    def test_arrives_naming_a_grant_the_profile_lacks_is_refused(self):
        """The map annotates the profile, so it cannot claim a grant the profile does not hold."""
        missing = next(a for a in SI.ABILITIES if a not in self.rec["prof"])
        path = self._write({self.key: self.rec}, {self.key: dict(self.arr, **{missing: 7})})
        with self.assertRaises(SI.SeedError):
            MB.merge([path], self.into)

    def test_a_level_one_arrival_is_refused(self):
        grant = next(iter(self.arr))
        path = self._write({self.key: self.rec}, {self.key: {grant: 1}})
        with self.assertRaises(SI.SeedError):
            MB.merge([path], self.into)

    def test_an_unassigned_subclass_is_refused(self):
        path = self._write({self.key: self.rec}, {self.key: self.arr})
        with self.assertRaises(SI.SeedError):
            MB.merge([path], self.into, expect=["some/Other Subclass"])

    def test_a_response_missing_a_half_is_refused(self):
        path = os.path.join(self.tmp, "half.json")
        with open(path, "w") as fh:
            json.dump({"bases": {self.key: self.rec}}, fh)
        with self.assertRaises(SI.SeedError):
            MB.merge([path], self.into)

    def test_two_responses_cannot_both_claim_a_subclass(self):
        a = self._write({self.key: self.rec}, {self.key: self.arr}, "a.json")
        b = self._write({self.key: self.rec}, {self.key: self.arr}, "b.json")
        with self.assertRaises(SI.SeedError):
            MB.merge([a, b], self.into)


class ArrivesValidation(unittest.TestCase):

    def test_the_published_file_validates(self):
        """`load_bases` now checks `arrives` too; the shipped file must still pass."""
        SI.load_bases(PUBLISHED)

    def test_an_unknown_grant_is_refused(self):
        bases = {"x/Y": {"verdict": "candidate", "prof": ["wis"], "boosters": []}}
        with self.assertRaises(SI.SeedError):
            SI.validate_arrives(bases, {"x/Y": {"telepathy": 7}})

    def test_a_level_outside_the_range_is_refused(self):
        bases = {"x/Y": {"verdict": "candidate", "prof": ["wis"], "boosters": []}}
        with self.assertRaises(SI.SeedError):
            SI.validate_arrives(bases, {"x/Y": {"wis": 21}})


if __name__ == "__main__":
    unittest.main()
