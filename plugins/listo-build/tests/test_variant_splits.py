"""A searched split is written straight into a seed, so it has to parse as one.

`enumerate_splits.py` used to append which class is taken first to the split string itself —
`Ranger 11 / Cleric 6 / Barbarian 3  [Barbarian first]`. `seed_index.check_split` cannot read that,
so every three-class variant the search produced was unwritable, and the fact was already carried
by `meta["first"]` anyway. Found when validating a variant-selection pass whose splits were copied
verbatim out of the variants file, exactly as intended.
"""
import os, sys, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "skills", "listo-ledger")
sys.path.insert(0, os.path.join(LEDGER, "scripts"))
import enumerate_splits as ES  # noqa: E402
import seed_index as SI  # noqa: E402


class Labels(unittest.TestCase):

    def test_the_annotation_is_gone_from_the_source(self):
        """A guard on the shape rather than the run, which takes six minutes."""
        with open(os.path.join(LEDGER, "scripts", "enumerate_splits.py")) as fh:
            src = fh.read()
        self.assertNotIn("first]", src,
                         "the level-1 class belongs in `meta['first']`, not in the split string")

    def test_a_composed_label_parses_as_a_seed_split(self):
        for text in ("Ranger 11 / Cleric 6 / Barbarian 3",
                     "Cleric 14 / Bard 6 (College of Stormcalling)",
                     "Fighter 11 / Rogue 3 / Wizard 6"):
            with self.subTest(split=text):
                self.assertEqual(sum(SI.check_split(text, "t").values()), 20)

    def test_the_old_annotated_form_is_refused(self):
        """Pinned so nobody reintroduces it believing `check_split` tolerates it."""
        with self.assertRaises(SI.SeedError):
            SI.check_split("Ranger 11 / Cleric 6 / Barbarian 3  [Barbarian first]", "t")

    def test_meta_still_carries_the_level_one_class(self):
        """Dropping it from the label is only safe while `meta` still records it."""
        with open(os.path.join(LEDGER, "scripts", "enumerate_splits.py")) as fh:
            self.assertIn('"first": first or primary', fh.read())


if __name__ == "__main__":
    unittest.main()
