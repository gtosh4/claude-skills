"""Pair prose is the expensive layer, so it should be commissioned from a diff, not wholesale.

The renderer already computes each chassis's best partner and already refuses to print prose that
names a partner the selection no longer chose. The report exposes that computation so a work plan
can ask for only the paragraphs that are actually wrong — and `prose_deps` is what stops the
answer being "the ones whose partner changed", which misses the entry whose partner stayed and
whose body did not.
"""
import copy, json, os, sys, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "skills", "listo-ledger")
sys.path.insert(0, os.path.join(LEDGER, "scripts"))
import render_ledger as RL  # noqa: E402

EXAMPLE = os.path.join(LEDGER, "assets", "ledger-example.json")


def ledger():
    """A copy of the worked example. Never the published ledger, and never mutated in place."""
    with open(EXAMPLE) as fh:
        return json.load(fh)


class Report(unittest.TestCase):

    def test_an_unchanged_ledger_schedules_nothing(self):
        rep = RL.selection_report(ledger(), ledger())
        self.assertEqual(rep["added"], [])
        self.assertEqual(rep["removed"], [])
        self.assertEqual(rep["partner_changed"], [])
        self.assertEqual(rep["evidence_moved"], [])
        self.assertTrue(all(e["status"] == "unchanged" for e in rep["entries"]))

    def test_every_entry_carries_a_partner_and_a_digest(self):
        rep = RL.selection_report(ledger())
        self.assertTrue(rep["entries"])
        for e in rep["entries"]:
            self.assertTrue(e["partner"])
            self.assertNotEqual(e["headliner"], e["partner"])
            self.assertEqual(len(e["prose_deps"]), 12)

    def test_missing_prose_is_reported_rather_than_rendered(self):
        d = ledger()
        first = RL.selection_report(d)["entries"][0]["headliner"]
        d["entries"].pop(first)
        self.assertIn(first, RL.selection_report(d)["prose_missing"])

    def test_chassis_prose_is_not_a_pair_prose_dependency(self):
        """Rewording a roster note must not schedule a pairing paragraph."""
        before = RL.selection_report(ledger())
        d = ledger()
        for cid in d["chassis"]:
            d["chassis"][cid]["note"] = "reworded, and saying the same thing"
            d["chassis"][cid]["strength"] = "also reworded"
        after = RL.selection_report(d, ledger())
        self.assertEqual(after["evidence_moved"], [])
        self.assertEqual([e["prose_deps"] for e in after["entries"]],
                         [e["prose_deps"] for e in before["entries"]])

    def test_evidence_moves_the_digest(self):
        d = ledger()
        who = RL.selection_report(d)["entries"][0]["headliner"]
        row = list(d["chassis"][who]["scores"]["II"])
        row[0] = max(0, row[0] - 1)
        d["chassis"][who]["scores"]["II"] = row
        rep = RL.selection_report(d, ledger())
        moved = set(rep["evidence_moved"]) | set(rep["partner_changed"]) | set(rep["added"])
        self.assertIn(who, moved)

    def test_rank_is_not_part_of_the_digest(self):
        """A pairing that slipped a place is the same pairing, and its prose still holds."""
        d = ledger()
        C = d["chassis"]
        import itertools
        field = sorted((RL.score(C, a, b) for a, b in itertools.combinations(C, 2)),
                       key=lambda r: -r["score"])
        sel = RL.select(d, field)
        me, other, rec = sel["kept"][0]
        first = RL.prose_deps(C, me, other, rec)
        again = RL.prose_deps(C, me, other, copy.deepcopy(rec))
        self.assertEqual(first, again)
        self.assertNotIn("rank", json.dumps(sel["kept"][0][2].get("blocks", {})))

    def test_the_template_version_schedules_a_review(self):
        before = RL.selection_report(ledger())
        RL.PROSE_TEMPLATE += 1
        self.addCleanup(setattr, RL, "PROSE_TEMPLATE", RL.PROSE_TEMPLATE - 1)
        after = RL.selection_report(ledger())
        self.assertNotEqual([e["prose_deps"] for e in after["entries"]],
                            [e["prose_deps"] for e in before["entries"]])


if __name__ == "__main__":
    unittest.main()
