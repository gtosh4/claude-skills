"""The three computed axes, pinned to the worked anchors in `axis-rubrics.md`.

§1, §2 and §3 are ratios against a fixed reference body, and each section ends in a table of
worked configurations with the ratio and the rung the author expects. Those tables are the spec's
own regression suite; nothing was checking them. A par table edited by one point, or a mitigation
term applied in the wrong order, moves every chassis in the ledger and every rung on every pair
sheet at once — silently, because a wrong ratio is indistinguishable from an honest one.
"""
import os, sys, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "skills", "listo-build", "scripts"))
import scoring as S  # noqa: E402


def st(act, raw, inst):
    """One single-target line, with the action budget filled by attacks."""
    block = {"actions": {"attacks": S.ACTION_BUDGET, "spells": 0, "filler": 0},
             "st_raw": raw, "st_instances": inst, "aoe_raw": 0.0, "aoe_instances": 0}
    return S.damage_terms(block, act)["st"]


def aoe(act, raw, inst):
    block = {"actions": {"attacks": 0, "spells": 2, "filler": S.ACTION_BUDGET - 2},
             "slots": {"to_damage": 0.5},
             "st_raw": 0.0, "st_instances": 0, "aoe_raw": raw, "aoe_instances": inst}
    return S.damage_terms(block, act)["aoe"]


def ehp(act, ac, pool=None, prop=(), flat=()):
    return S.derive_ehp({"pool": S.PAR_POOL[act] if pool is None else pool, "ac": ac,
                         "prop": [list(p) for p in prop], "flat": [list(f) for f in flat]}, act)


class SingleTarget(unittest.TestCase):
    """axis-rubrics.md §1, "Worked anchors"."""

    def test_extra_attack_with_no_rider_is_par_in_act_one_and_outrun_after(self):
        for act, hit, scored, rung in (("I", 12, 60, 2), ("II", 12, 68, 1), ("III", 13, 84, 1)):
            r = st(act, 4 * hit, 4)
            self.assertAlmostEqual(r["scored"], scored, delta=0.5, msg=act)
            self.assertEqual(r["rung"], rung, act)

    def test_a_flat_rider_decays_across_the_run_with_nothing_having_changed(self):
        # 1d6 on four attacks: 1.23x par in Act I and 0.80x in Act III. The decay is the
        # arithmetic's, not a hand-written rule, and `k` does not rescue it — it lands on the
        # same four instances par has, so it cancels.
        got = [st(act, 4 * (hit + 3.5), 4)["rung"] for act, hit in (("I", 12), ("II", 12), ("III", 13))]
        self.assertEqual(got, [3, 2, 1])

    def test_gear_pays_per_instance_so_eight_small_rolls_collect_it_twice_over(self):
        # A character-20 body firing eight Eldritch Blast beams: ~60 raw from two Warlock levels,
        # eight instances, which `k` takes to 124 — 1.01x par where the gear-free read is 0.79x.
        r = st("III", 60.0, 8)
        self.assertAlmostEqual(r["scored"], 124.0, delta=0.5)
        self.assertAlmostEqual(r["ratio"], 1.01, places=2)
        self.assertAlmostEqual(60.0 / r["par"], 0.49, places=2)


class Area(unittest.TestCase):
    """axis-rubrics.md §2, "Worked anchors"."""

    def test_one_fireball_a_fight_is_rung_one_in_every_act(self):
        # 8d6 on four targets, save for half, spread over four rounds: one instance a round.
        for act in S.ACTS:
            r = aoe(act, 28 * 0.775, 1)
            self.assertEqual(r["rung"], 1, act)

    def test_at_will_area_damage_outruns_a_once_a_fight_burst_by_a_wide_margin(self):
        # Eldritch Cone, at-will, x2 Actions, frozen at 16.5 from character 10: 142 -> 2.18x in
        # Act II and 166 -> 2.02x in Act III. Record the decay; do not invent a rung drop.
        two, three = aoe("II", 142 - 5 * 8, 8), aoe("III", 166 - 8 * 8, 8)
        self.assertAlmostEqual(two["ratio"], 2.18, places=2)
        self.assertAlmostEqual(three["ratio"], 2.02, places=2)
        self.assertEqual([two["rung"], three["rung"]], [4, 4])

    def test_the_bands_are_wider_than_the_single_target_ones(self):
        # A ratio that is a damage chassis on §1 is merely ahead on §2.
        self.assertEqual(S.ratio_rung(1.6, "st"), 4)
        self.assertEqual(S.ratio_rung(1.6, "aoe"), 3)


class EffectiveHP(unittest.TestCase):
    """axis-rubrics.md §3, "Worked anchors, Act III"."""

    def test_the_ac_ladder_reproduces_the_rubrics_act_three_table(self):
        for ac, ratio, rung in ((14, 0.81, 1), (17, 1.00, 2), (18, 1.08, 2),
                                (19, 1.18, 3), (20, 1.30, 3)):
            r = ehp("III", ac)
            self.assertAlmostEqual(r["ratio"], ratio, places=2, msg="AC %d" % ac)
            self.assertEqual(r["rung"], rung, "AC %d" % ac)

    def test_flat_reduction_is_worth_far_more_against_a_crowd_than_against_a_boss(self):
        # Heavy Armour Master's -5 on AC 20: x1.61 crowd, x1.14 boss, blending to 1.79 -> rung 4.
        r = ehp("III", 20, flat=[("Heavy Armour Master", 5)])
        crowd, boss = r["fights"]
        self.assertAlmostEqual(crowd["flat_mult"], 1.61, delta=0.01)
        self.assertAlmostEqual(boss["flat_mult"], 1.14, places=2)
        self.assertAlmostEqual(r["ratio"], 1.79, delta=0.02)
        self.assertEqual(r["rung"], 4)

    def test_a_proportional_layer_reaches_the_acts_ceiling_where_a_flat_one_does_not(self):
        self.assertEqual(ehp("III", 20, prop=[("Shield Master Block", 0.5)])["rung"], 5)

    def test_par_is_par_in_every_act(self):
        for act in S.ACTS:
            self.assertAlmostEqual(ehp(act, S.PAR_AC)["ratio"], 1.0, places=6, msg=act)

    def test_the_flat_term_is_clamped_so_one_aura_cannot_read_as_four_times_par(self):
        # Aura of Moonlight against Act I's crowd hit of 5.4 returns a multiplier above 13
        # unclamped. The v7 roster clamped it by hand at x3; the clamp is the model's now.
        r = ehp("I", S.PAR_AC, flat=[("Aura of Moonlight", 5)])
        crowd = r["fights"][0]
        self.assertTrue(crowd["capped"])
        self.assertAlmostEqual(crowd["flat_mult"], S.MIT_CAP, places=6)

    def test_p_hit_clamps_at_the_natural_twenty_floor(self):
        self.assertAlmostEqual(ehp("III", 40)["p_hit"], S.P_HIT_MIN, places=6)


class FailsClosed(unittest.TestCase):

    def test_a_proportional_factor_authored_as_a_multiplier_is_refused(self):
        # "Halves the hit" written as 2 would score a body taking DOUBLE damage as durable.
        with self.assertRaises(S.ScoringError):
            ehp("III", 19, prop=[("resistance", 2.0)])

    def test_negative_flat_reduction_is_refused(self):
        with self.assertRaises(S.ScoringError):
            ehp("III", 19, flat=[("resistance", -5)])

    def test_a_missing_pool_is_refused_rather_than_defaulted_to_par(self):
        with self.assertRaises(S.ScoringError):
            S.derive_ehp({"ac": 19}, "III")

    def test_the_worked_terms_agree_with_the_rung_the_ledger_takes(self):
        # `damage_terms` must not become a second calculation that happens to agree.
        block = {"actions": {"attacks": S.ACTION_BUDGET, "spells": 0, "filler": 0},
                 "st_raw": 96.0, "st_instances": 6, "aoe_raw": 40.0, "aoe_instances": 4}
        st_rung, aoe_rung, st_scored, aoe_scored = S.derive_damage(block, "II")
        terms = S.damage_terms(block, "II")
        self.assertEqual((terms["st"]["rung"], terms["aoe"]["rung"]), (st_rung, aoe_rung))
        self.assertEqual((terms["st"]["scored"], terms["aoe"]["scored"]), (st_scored, aoe_scored))


if __name__ == "__main__":
    unittest.main()
