"""The three cache stages go stale independently, and that independence is the point.

A seed is a judgement about a subclass under the sweep brief. Enumeration is a judgement about
which split of that subclass is worth scoring, under the two catalogues. A score is a judgement
about the resulting body under the rubric. Editing any one of the three must not schedule the
other two — the whole reason `DEPS` is keyed by stage rather than by "something changed".
"""
import os, shutil, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "skills", "listo-ledger")
sys.path.insert(0, os.path.join(LEDGER, "scripts"))
import seed_index as SI  # noqa: E402


class Stages(unittest.TestCase):
    """Every test runs against copied dependency files, never the published ones."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        self._deps = SI.DEPS
        self.addCleanup(setattr, SI, "DEPS", self._deps)
        # Copy every dependency file into the fixture directory under its own basename, then
        # point DEPS at the copies. Editing a copy is what these tests do; editing the original
        # would invalidate the real roster's caches from a test run.
        SI.DEPS = {stage: [self._copy(p) for p in paths]
                   for stage, paths in self._deps.items()}
        self.inv = self._one_subclass()

    def _copy(self, path):
        dst = os.path.join(self.tmp, os.path.basename(path))
        shutil.copyfile(path, dst)
        return dst

    def _one_subclass(self):
        """One real class and one real subclass — `digests()` reads the actual class files."""
        inv = SI.inventory()
        cls = sorted(inv)[0]
        return {cls: [inv[cls][0]]}

    def _seeds(self):
        """One promoted build, stamped current at all three stages."""
        (cls, subs), = self.inv.items()
        key = f"{cls}/{subs[0]}"
        return {key: {"verdict": "candidate",
                      "src": SI.digests(cls)[subs[0]],
                      "seed_deps": SI.deps_hash("seed"),
                      "builds": {"lockdown": {"split": f"{cls.title()} 20",
                                              "score_deps": SI.deps_hash("score"),
                                              "split_deps": SI.deps_hash("split")}}}}, key

    def _touch(self, stage, path_name):
        """Append a byte to one fixture file, the way a real edit moves its digest."""
        (path,) = [p for p in SI.DEPS[stage] if os.path.basename(p) == path_name]
        with open(path, "a") as fh:
            fh.write("\n<!-- edited by a test -->\n")

    def test_everything_stamped_is_quiet(self):
        seeds, _ = self._seeds()
        rep = SI.audit(self.inv, seeds)
        for bucket in ("unseeded", "stale", "drifted", "rules",
                       "unscored", "rescore", "unenumerated", "reenumerate"):
            self.assertEqual(rep[bucket], [], f"{bucket} should be empty on an unchanged tree")

    def test_dip_catalogue_edit_is_enumeration_only(self):
        seeds, key = self._seeds()
        self._touch("split", "dip-catalogue.json")
        rep = SI.audit(self.inv, seeds)
        self.assertEqual(rep["reenumerate"], [f"{key}:lockdown"])
        # The seed is a judgement about the subclass, not about what the dip catalogue sells.
        self.assertEqual(rep["drifted"], [])
        self.assertEqual(rep["rules"], [])
        # And the score of the exact old body is still a true statement about that body. A new
        # split may be selected downstream; that is what re-running the search decides.
        self.assertEqual(rep["rescore"], [])
        self.assertEqual(rep["unscored"], [])

    def test_base_profile_edit_is_enumeration_only(self):
        seeds, key = self._seeds()
        self._touch("split", "subclass-bases.json")
        rep = SI.audit(self.inv, seeds)
        self.assertEqual(rep["reenumerate"], [f"{key}:lockdown"])
        self.assertEqual(rep["rescore"], [])

    def test_rubric_edit_is_scoring_only(self):
        seeds, key = self._seeds()
        self._touch("score", "axis-rubrics.md")
        rep = SI.audit(self.inv, seeds)
        self.assertEqual(rep["rescore"], [f"{key}:lockdown"])
        self.assertEqual(rep["reenumerate"], [])
        self.assertEqual(rep["drifted"], [])
        self.assertEqual(rep["rules"], [])

    def test_sweep_brief_edit_is_seeding_only(self):
        seeds, key = self._seeds()
        self._touch("seed", "sweep-brief.md")
        rep = SI.audit(self.inv, seeds)
        self.assertEqual(rep["rules"], [key])
        # A build whose seed must be redone is not also reported as needing a re-score or a
        # re-enumeration: the seed comes first, and the rest may be moot once it is redone.
        self.assertEqual(rep["rescore"], [])
        self.assertEqual(rep["reenumerate"], [])

    def test_unstamped_build_fails_closed(self):
        seeds, key = self._seeds()
        del seeds[key]["builds"]["lockdown"]["split_deps"]
        rep = SI.audit(self.inv, seeds)
        self.assertEqual(rep["unenumerated"], [f"{key}:lockdown"])
        self.assertEqual(rep["reenumerate"], [])


class AddrList(unittest.TestCase):
    """`--scored` / `--enumerated` work-lists."""

    def test_all_is_the_promoted_roster(self):
        seeds = {"cleric/Tempest": {"verdict": "candidate",
                                    "builds": {"lockdown": {"split": "Cleric 20"}}}}
        self.assertEqual(SI.addr_list("all", seeds), ["cleric/Tempest:lockdown"])

    def test_at_file_takes_one_address_per_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "addrs")
            with open(path, "w") as fh:
                fh.write("fighter/Banneret (Purple Dragon Knight, 2014):front-line\n\n")
            self.assertEqual(SI.addr_list("@" + path, {}),
                             ["fighter/Banneret (Purple Dragon Knight, 2014):front-line"])


if __name__ == "__main__":
    unittest.main()
