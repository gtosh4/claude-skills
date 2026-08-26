"""`damage.mult` is the pair sheet's re-score, and it has to be bounded.

The field was documented in `pair-schema.md` and applied in `derive_damage` before this test
existed, but its only guard was `m > 0`. That accepts 5.0. An accuracy correction is the one term
par cannot answer — `axis-rubrics.md`'s constants table prices advantage at x1.35 and its mirror,
disadvantage, at x0.65, and nothing outside that pair — so an unbounded multiplier is exactly the
unfalsifiable number the v7 damage block was built to refuse. A misspelt axis key was worse than
unbounded: it applied nothing and scored as though the correction had been honest.

Also pins the two things a reader of the rendered sheet depends on: that the multiplier lands
AFTER the gear constant (the rider rides the same roll, so a miss deals none of it), and that the
figure `damage_terms` displays is the figure the rung was taken against.
"""
import os, sys, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "skills", "listo-build", "scripts"))
import scoring as S  # noqa: E402


def block(**kw):
    """A minimal valid Act III damage block: four attacks a round, nothing else."""
    b = {"actions": {"attacks": 8, "spells": 0, "filler": 0},
         "st_raw": 100.0, "st_instances": 4.0,
         "aoe_raw": 80.0, "aoe_instances": 4.0}
    b.update(kw)
    return b


WHY = "Snowlight blind engine (CON save) — target-side advantage the partner supplies"


class MultBounds(unittest.TestCase):

    def test_ceiling_and_floor_are_the_rubric_constants(self):
        self.assertEqual(S.MULT_CEIL, 1.35)
        self.assertEqual(S.MULT_FLOOR, 0.65)
        self.assertEqual(S.ACC_MULT[2], S.MULT_CEIL)

    def test_above_the_ceiling_is_refused(self):
        with self.assertRaises(S.ScoringError):
            S.derive_damage(block(mult={"st": 1.6, "why": WHY}), "III")

    def test_below_the_floor_is_refused(self):
        with self.assertRaises(S.ScoringError):
            S.derive_damage(block(mult={"st": 0.5, "why": WHY}), "III")

    def test_the_disadvantage_mirror_is_legal(self):
        S.derive_damage(block(mult={"st": 0.65, "why": "element-locked into a resisted type"}), "III")

    def test_a_multiplier_needs_a_why(self):
        with self.assertRaises(S.ScoringError):
            S.derive_damage(block(mult={"st": 1.35}), "III")
        with self.assertRaises(S.ScoringError):
            S.derive_damage(block(mult={"st": 1.35, "why": "   "}), "III")

    def test_unity_needs_no_why(self):
        S.derive_damage(block(mult={"st": 1.0, "aoe": 1.0}), "III")

    def test_a_misspelt_axis_is_refused_rather_than_ignored(self):
        with self.assertRaises(S.ScoringError):
            S.derive_damage(block(mult={"melee": 1.35, "why": WHY}), "III")

    def test_a_bool_is_not_a_multiplier(self):
        # float(True) is 1.0, so coercion would have swallowed this silently.
        with self.assertRaises(S.ScoringError):
            S.derive_damage(block(mult={"st": True, "why": WHY}), "III")


class MultArithmetic(unittest.TestCase):

    def test_it_lands_after_the_gear_constant(self):
        _, _, st, _ = S.derive_damage(block(mult={"st": 1.35, "why": WHY}), "III")
        # raw 100 + 4 instances x k 8 = 132, then x1.35 — not 100 x 1.35 + 32.
        self.assertAlmostEqual(st, (100.0 + 4 * S.GEAR["III"]) * 1.35)

    def test_it_is_applied_exactly_once(self):
        _, _, bare, _ = S.derive_damage(block(), "III")
        _, _, mult, _ = S.derive_damage(block(mult={"st": 1.19, "why": WHY}), "III")
        self.assertAlmostEqual(mult / bare, 1.19)

    def test_each_axis_moves_on_its_own(self):
        _, _, st, aoe = S.derive_damage(block(mult={"st": 1.35, "why": WHY}), "III")
        self.assertAlmostEqual(st, (100.0 + 4 * S.GEAR["III"]) * 1.35)
        self.assertAlmostEqual(aoe, 80.0 + 4 * S.GEAR["III"])

    def test_the_displayed_figure_is_the_one_the_rung_was_taken_against(self):
        b = block(mult={"st": 1.19, "aoe": 1.19, "why": WHY})
        st_rung, aoe_rung, st, aoe = S.derive_damage(b, "III")
        terms = S.damage_terms(b, "III")
        for axis, rung, scored in (("st", st_rung, st), ("aoe", aoe_rung, aoe)):
            self.assertAlmostEqual(terms[axis]["scored"], scored)
            self.assertAlmostEqual(terms[axis]["ratio"], scored / S.PAR[axis]["III"])
            self.assertEqual(terms[axis]["rung"], rung)


class LedgerRecordsScoreABodyAlone(unittest.TestCase):
    """`mult` is a property of a pairing. A chassis carrying one claims a buff it only has next
    to one specific partner — the objection rule 1 raises against named items."""

    def chassis(self, **dmg):
        nulls = [None, None, 3, 3, 2, 2, 2, 3, None, 3]
        return {"split": "Fighter 20 (Champion)", "reach": "mobile", "types": ["slashing"],
                "saves": {a: {"prof": ["str", "con"], "boosters": []} for a in S.ACTS},
                "scores": {a: list(nulls) for a in S.ACTS},
                "damage": {a: block(**dmg) for a in S.ACTS},
                "skills": {a: {k: 5 for k in S.RECORDED_SKILLS} for a in S.ACTS},
                "note": "x", "strength": "x", "weakness": "x"}

    def test_a_clean_record_validates(self):
        S.validate_chassis("Probe", self.chassis())

    def test_a_record_carrying_mult_is_refused(self):
        with self.assertRaises(S.ScoringError):
            S.validate_chassis("Probe", self.chassis(mult={"st": 1.35, "why": WHY}))


class AccuracyRegistry(unittest.TestCase):

    def test_every_effect_names_a_known_tier(self):
        for eff, spec in S.ACCURACY.items():
            self.assertIn(spec["tier"], S.ACC_MULT, f"{eff} names an unpriced tier")

    def test_tier_one_is_the_save_gated_share_of_tier_two(self):
        # 1 + 0.35 x s at the rubric's act-invariant s = 0.55.
        self.assertAlmostEqual(S.ACC_MULT[1], 1.0 + (S.ACC_MULT[2] - 1.0) * 0.55, places=2)


if __name__ == "__main__":
    unittest.main()
