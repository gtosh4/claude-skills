"""The scoring pass's read set, measured rather than argued about.

The sweep has a cost model and agent count is its dial. Scoring never had one, so "make scoring
cheaper" was a discussion about a number nobody had. This pins the shape of the answer: what every
agent pays, what the roster pays once, and that the two are never conflated with each other or
with a token count that was really a byte count.
"""
import os, sys, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "skills", "listo-ledger")
sys.path.insert(0, os.path.join(LEDGER, "scripts"))
import read_cost as RC  # noqa: E402

SPLITS = ["Cleric 14 (Tempest) / Sorcerer 6 (Storm Sorcery)",
          "Cleric 17 (Death) / Fighter 3 (Battle Master)"]
ADDRS = ["cleric/Tempest:lockdown", "cleric/Death:action-economy"]


class Cost(unittest.TestCase):

    def test_the_shared_set_is_charged_once_per_agent(self):
        one = RC.report(ADDRS, SPLITS, 1)
        four = RC.report(ADDRS, SPLITS, 4)
        shared = one["shared"]["bytes"]
        self.assertEqual(four["read_total_bytes"] - one["read_total_bytes"], shared * 3)

    def test_the_assigned_read_is_charged_once(self):
        one = RC.report(ADDRS, SPLITS, 1)
        four = RC.report(ADDRS, SPLITS, 4)
        self.assertEqual(one["assigned"]["unique_bytes"], four["assigned"]["unique_bytes"])

    def test_two_chassis_sharing_a_class_share_its_sections(self):
        """Both splits are Cleric-dominant, so the at-a-glance block is read once, not twice."""
        rep = RC.assigned_cost(ADDRS, SPLITS)
        self.assertLess(rep["unique_bytes"], rep["naive_sum_bytes"],
                        "class-coherent batching is only worth something if this holds")

    def test_bytes_and_token_estimates_are_kept_apart(self):
        rep = RC.report(ADDRS, SPLITS, 1)
        self.assertIn("ESTIMATE", rep["note"])
        self.assertNotEqual(rep["shared"]["bytes"], rep["shared"]["tokens_estimate"])
        self.assertTrue(rep["unmeasured"], "what a run must supply has to stay named")


if __name__ == "__main__":
    unittest.main()
