"""One file per chassis, so an interrupted scoring turn costs a turn and not a batch.

The old contract made the agent's final message both the data and the thing subject to the turn's
output limit. A batch that ran long was lost whole; one had to be hand-split into halves to fit.
These tests pin the properties that removes: resume skips valid work, `.tmp` files are never read
as results, two addresses that slug identically get distinct paths, and a stale result is only
replaced by a candidate that validates.
"""
import copy, json, os, shutil, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "skills", "listo-ledger")
sys.path.insert(0, os.path.join(LEDGER, "scripts"))
import result_store as RS  # noqa: E402
import merge_results as MR  # noqa: E402
import score_deps as SD  # noqa: E402
import seed_index as SI  # noqa: E402
from scoring import ScoringError  # noqa: E402

A1 = "cleric/Death:action-economy"
S1 = "Cleric 17 (Death) / Fighter 3 (Battle Master)"
A2 = "cleric/Life:durability"
S2 = "Cleric 14 (Life) / Paladin 6 (Oath of Devotion)"


def damage(**over):
    """The smallest block that validates: eight action-slots spent, both raws instanced."""
    blk = {"actions": {"attacks": 6, "spells": 0, "filler": 2},
           "st_raw": 70, "aoe_raw": 40, "st_instances": 6, "aoe_instances": 4}
    blk.update(over)
    return blk


def record(split, note="A body.", **over):
    rec = {"proposed_id": "Testbody", "split": split, "reach": "hybrid",
           "concentration": True, "types": ["necrotic"], "meta": "Wis 22 · 7 feats",
           "saves": {a: {"prof": ["wis", "cha"], "boosters": []} for a in RS.ACTS},
           # Indices 0 and 1 are derived from `damage`, exactly as index 8 is from `saves`.
           "scores": {a: [None, None, 3, 2, 2, 1, 0, 3, None, 4] for a in RS.ACTS},
           "damage": {a: damage() for a in RS.ACTS},
           "note": note, "strength": "Two actions.", "wants": "Concentration.",
           "uncertain": []}
    rec.update(over)
    return rec


class Store(unittest.TestCase):

    def setUp(self):
        self.run = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.run)
        self.man = RS.write_manifest(self.run, "score-001", [(A1, S1), (A2, S2)])

    def test_status_starts_empty_and_tracks_progress(self):
        st = RS.status(self.run, "score-001")
        self.assertEqual((st["completed"], st["remaining"]), (0, 2))
        RS.put(self.run, "score-001", A1, record(S1))
        st = RS.status(self.run, "score-001")
        self.assertEqual(st["valid"], [A1])
        self.assertEqual(st["missing"], [A2])

    def test_an_interrupted_turn_loses_nothing(self):
        """The acceptance gate: put one, drop a half-written file, resume."""
        RS.put(self.run, "score-001", A1, record(S1))
        res = os.path.join(self.run, "results", "score-001")
        with open(os.path.join(res, RS.filename(A2) + ".tmp"), "w") as fh:
            fh.write('{"format": 1, "record": {"note": "half a th')
        st = RS.status(self.run, "score-001")
        self.assertEqual(st["valid"], [A1], "completed work must survive the interruption")
        self.assertEqual(st["missing"], [A2], "the half-written file is not a result")
        self.assertEqual(len(st["interrupted"]), 1)
        self.assertEqual(st["problems"], [])
        RS.put(self.run, "score-001", A2, record(S2))
        self.assertEqual(RS.status(self.run, "score-001")["remaining"], 0)

    def test_a_corrupt_temp_file_is_never_merged(self):
        for addr, split in ((A1, S1), (A2, S2)):
            RS.put(self.run, "score-001", addr, record(split))
        res = os.path.join(self.run, "results", "score-001")
        with open(os.path.join(res, RS.filename(A1) + ".tmp"), "w") as fh:
            fh.write("not json at all")
        got, problems = RS.read_results(self.run, "score-001")
        self.assertEqual(sorted(got), sorted([A1, A2]))
        self.assertEqual(problems, [])

    def test_addresses_that_slug_alike_get_distinct_paths(self):
        a = "fighter/Banneret (Purple Dragon Knight, 2014):front-line"
        b = "fighter/Banneret Purple Dragon Knight 2014:front-line"
        self.assertEqual(RS.filename(a).split("--")[0], RS.filename(b).split("--")[0],
                         "the readable half is expected to be lossy — that is why the digest exists")
        self.assertNotEqual(RS.filename(a), RS.filename(b))

    def test_a_valid_result_is_not_rewritten(self):
        path = RS.put(self.run, "score-001", A1, record(S1, note="first"))
        RS.put(self.run, "score-001", A1, record(S1, note="second"))
        with open(path) as fh:
            self.assertEqual(json.load(fh)["record"]["note"], "first")

    def test_a_stale_result_is_replaced_only_by_a_valid_candidate(self):
        path = RS.put(self.run, "score-001", A1, record(S1, note="first"))
        # Move a recorded dependency, the way editing the secondary class would.
        with open(path) as fh:
            doc = json.load(fh)
        doc["deps"]["judgment_rules"] = "0" * 12
        with open(path, "w") as fh:
            json.dump(doc, fh)
        st = RS.status(self.run, "score-001")
        self.assertEqual(st["stale"], [A1])
        with self.assertRaises(RS.StoreError):
            RS.put(self.run, "score-001", A1, record(S1, types=[]))
        with open(path) as fh:
            self.assertEqual(json.load(fh)["record"]["note"], "first",
                             "a rejected candidate must not destroy the result it would replace")
        RS.put(self.run, "score-001", A1, record(S1, note="second"))
        with open(path) as fh:
            self.assertEqual(json.load(fh)["record"]["note"], "second")

    def test_an_address_outside_the_assignment_is_refused(self):
        with self.assertRaises(RS.StoreError):
            RS.put(self.run, "score-001", "wizard/Evocation:lockdown", record(S1))

    def test_a_split_that_disagrees_with_the_assignment_is_refused(self):
        with self.assertRaises(RS.StoreError):
            RS.put(self.run, "score-001", A1, record(S2))

    def test_validation_rejects_an_authored_saves_rung(self):
        rec = record(S1)
        rec["scores"]["II"] = [None, None, 3, 2, 2, 1, 0, 3, 4, 4]
        with self.assertRaises(RS.StoreError):
            RS.put(self.run, "score-001", A1, rec)

    def test_validation_rejects_a_null_skills_rung(self):
        rec = record(S1)
        rec["scores"]["II"] = [None, None, 3, 2, 2, 1, 0, None, None, 4]
        with self.assertRaises(RS.StoreError):
            RS.put(self.run, "score-001", A1, rec)


class DerivedDamage(unittest.TestCase):
    """The damage axes are arithmetic, and the store is where the agent can still fix it.

    v6 stored a rung and nothing else, so an authored `2` could not be re-checked from outside and
    the whole roster was stranded when the AoE par was re-based. The block records what the rung was
    taken against. Every check below is a defect that shipped in v6.
    """

    def setUp(self):
        self.run = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.run)
        RS.write_manifest(self.run, "score-001", [(A1, S1), (A2, S2)])

    def test_an_authored_damage_rung_is_refused(self):
        """The v6 shape must not slip through: it is the thing this version exists to replace."""
        rec = record(S1)
        rec["scores"]["II"] = [3, 2, 3, 2, 2, 1, 0, 3, None, 4]
        with self.assertRaises(RS.StoreError) as e:
            RS.put(self.run, "score-001", A1, rec)
        self.assertIn("null", str(e.exception))

    def test_a_missing_act_block_is_refused(self):
        rec = record(S1)
        del rec["damage"]["II"]
        with self.assertRaises(RS.StoreError):
            RS.put(self.run, "score-001", A1, rec)

    def test_a_record_with_no_damage_at_all_is_refused(self):
        rec = record(S1)
        del rec["damage"]
        with self.assertRaises(RS.StoreError):
            RS.put(self.run, "score-001", A1, rec)

    def test_unconserved_actions_are_caught_where_they_were_written(self):
        """A caster with 3.7 casts left 4.3 slots unscored in v6, and nothing noticed."""
        rec = record(S1, damage={a: damage(actions={"attacks": 0, "spells": 3.7, "filler": 0})
                                 for a in RS.ACTS})
        with self.assertRaises(ScoringError):
            RS.put(self.run, "score-001", A1, rec)

    def test_a_raw_with_no_instance_count_is_refused(self):
        """Gear attaches per damage roll, so the count is stated rather than inferred."""
        blk = damage()
        del blk["st_instances"]
        rec = record(S1, damage={a: blk for a in RS.ACTS})
        with self.assertRaises(ScoringError):
            RS.put(self.run, "score-001", A1, rec)

    def test_a_short_rest_pool_underspent_without_a_reason_is_refused(self):
        rec = record(S1, damage={a: damage(pools=[{"name": "ki", "refresh": "short",
                                                   "size": 4, "spent": 1}]) for a in RS.ACTS})
        with self.assertRaises(ScoringError):
            RS.put(self.run, "score-001", A1, rec)
        rec = record(S1, damage={a: damage(pools=[{"name": "ki", "refresh": "short", "size": 4,
                                                   "spent": 1, "underspend_reason": "actions bind"}])
                                 for a in RS.ACTS})
        RS.put(self.run, "score-001", A1, rec)

    def test_the_block_survives_the_merge(self):
        """`merge_results` carries `damage`, or the merged ledger cannot re-derive its own rungs."""
        for addr, split in ((A1, S1), (A2, S2)):
            RS.put(self.run, "score-001", addr, record(split, skills=SKILLS))
        merged, _report = MR.merge(self.run)
        cid = next(k for k, v in merged["chassis"].items() if v["address"] == A1)
        self.assertEqual(merged["chassis"][cid]["damage"]["II"]["st_instances"], 6)
        self.assertIsNone(merged["chassis"][cid]["scores"]["II"][RS.ST_IDX])

    def test_a_meta_that_names_no_ability_is_refused(self):
        """`gear_key` declines rather than guessing, so the contention factor goes silently coarse."""
        rec = record(S1, meta="7 feats")
        with self.assertRaises(RS.StoreError) as e:
            RS.put(self.run, "score-001", A1, rec)
        self.assertIn("meta", str(e.exception))


SKILLS = {"I": {"Perception": 5, "Investigation": 1, "Persuasion": 4},
          "II": {"Perception": 7, "Investigation": 2, "Persuasion": 6},
          "III": {"Perception": 8, "Investigation": 3, "Persuasion": 8}}


class Unified(unittest.TestCase):
    """One pass authors the scores AND the evidence, instead of three passes rebuilding the body."""

    def setUp(self):
        self.run = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.run)
        RS.write_manifest(self.run, "score-001", [(A1, S1)], unified=True)

    def test_a_score_only_record_is_refused(self):
        with self.assertRaises(RS.StoreError):
            RS.put(self.run, "score-001", A1, record(S1))

    def test_a_complete_record_lands(self):
        RS.put(self.run, "score-001", A1, record(S1, skills=SKILLS))
        self.assertEqual(RS.status(self.run, "score-001")["valid"], [A1])

    def test_a_missing_mandatory_skill_is_refused(self):
        skills = copy.deepcopy(SKILLS)
        del skills["II"]["Persuasion"]
        with self.assertRaises(RS.StoreError):
            RS.put(self.run, "score-001", A1, record(S1, skills=skills))

    def test_an_unknown_skill_is_refused(self):
        skills = copy.deepcopy(SKILLS)
        skills["I"]["Basketweaving"] = 4
        with self.assertRaises(RS.StoreError):
            RS.put(self.run, "score-001", A1, record(S1, skills=skills))

    def test_a_falling_series_is_refused(self):
        """The proficiency bonus rises +3/+4/+5 and abilities only go up."""
        skills = copy.deepcopy(SKILLS)
        skills["III"]["Perception"] = 6
        with self.assertRaises(RS.StoreError):
            RS.put(self.run, "score-001", A1, record(S1, skills=skills))

    def test_the_evidence_reaches_the_merged_record(self):
        RS.put(self.run, "score-001", A1, record(S1, skills=SKILLS))
        merged, report = MR.merge(self.run)
        cid = report["merged"][0]["chassis"]
        self.assertEqual(merged["chassis"][cid]["skills"], SKILLS)
        self.assertEqual(report["evidence_gaps"], [],
                         "a unified pass leaves no evidence gap behind")

    def test_a_split_pass_still_leaves_the_published_map_alone(self):
        """The guard that lets both contracts coexist during the parity trial."""
        run = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, run)
        RS.write_manifest(run, "score-001", [(A1, S1)], unified=False)
        RS.put(run, "score-001", A1, record(S1))
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "ledger.json")
            with open(path, "w") as fh:
                json.dump({"chassis": {"Reaper": {"address": A1, "skills": SKILLS}}}, fh)
            merged, _rep = MR.merge(run, into=path)
        self.assertEqual(merged["chassis"]["Reaper"]["skills"], SKILLS)


class Merge(unittest.TestCase):

    def setUp(self):
        self.run = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.run)
        RS.write_manifest(self.run, "score-001", [(A1, S1), (A2, S2)])
        self.seeds = SI.load(os.path.join(LEDGER, "assets", "chassis-seeds.json"))

    def _ledger(self):
        """A stand-in for the published ledger: one body, carrying its address and an
        evidence-pass field the scoring pass does not own."""
        ids = {A1: "Reaper"}
        return {"chassis": {ids[A1]: {"address": A1, "split": S1, "note": "old", "skills":
                                      {a: {"Perception": 5, "Investigation": 1, "Persuasion": 4}
                                       for a in RS.ACTS}}}}, ids

    def test_a_missing_address_refuses_to_merge(self):
        RS.put(self.run, "score-001", A1, record(S1))
        with self.assertRaises(RS.StoreError):
            MR.merge(self.run)
        report = MR.merge(self.run, partial=True)[1]
        self.assertEqual(report["missing"], [A2])

    def test_published_ids_stay_put_and_unowned_fields_survive(self):
        ledger, ids = self._ledger()
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "ledger.json")
            with open(path, "w") as fh:
                json.dump(ledger, fh)
            RS.put(self.run, "score-001", A1, record(S1, note="new"))
            merged, report = MR.merge(self.run, into=path, partial=True)
        cid = ids[A1]
        self.assertIn(cid, merged["chassis"], "a re-score must not orphan the published id")
        self.assertEqual(merged["chassis"][cid]["note"], "new")
        self.assertIn("skills", merged["chassis"][cid],
                      "`skills` belongs to the evidence passes and must survive a re-score")
        self.assertEqual(report["changed"][cid]["note"], ["old", "new"])
        self.assertEqual(report["evidence_gaps"], [])

    def test_a_chassis_with_no_skills_map_is_reported_as_an_evidence_gap(self):
        RS.put(self.run, "score-001", A1, record(S1))
        report = MR.merge(self.run, partial=True)[1]
        self.assertEqual(report["evidence_gaps"], [A1])

    def test_a_stale_result_blocks_the_merge(self):
        path = RS.put(self.run, "score-001", A1, record(S1))
        with open(path) as fh:
            doc = json.load(fh)
        doc["deps"]["schema"] = "0" * 12
        with open(path, "w") as fh:
            json.dump(doc, fh)
        with self.assertRaises(RS.StoreError):
            MR.merge(self.run, partial=True)

    def test_a_hand_written_file_under_the_wrong_name_is_a_problem(self):
        RS.put(self.run, "score-001", A1, record(S1))
        res = os.path.join(self.run, "results", "score-001")
        with open(os.path.join(res, RS.filename(A1))) as fh:
            doc = json.load(fh)
        # A1's document, dropped in under A2's filename. The filename is derived from the
        # address, so the two disagreeing means something wrote by hand.
        forged = copy.deepcopy(doc)
        with open(os.path.join(res, RS.filename(A2)), "w") as fh:
            json.dump(forged, fh)
        got, problems = RS.read_results(self.run, "score-001")
        self.assertEqual(len(problems), 1)
        self.assertIn(A1, problems[0])
        self.assertNotIn(A2, got, "a forged result must not stand in for the address it names")


if __name__ == "__main__":
    unittest.main()
