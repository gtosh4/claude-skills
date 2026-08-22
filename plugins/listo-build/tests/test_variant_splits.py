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


class PrimaryClass(unittest.TestCase):
    """`audit_roster` groups by primary class, so the key has to survive how a split spells it.

    Matching one word before the number truncated every multi-word class name to its last word:
    `Blood Hunter 17` grouped as "Hunter" and `Bloodhunter 14` as "Bloodhunter", splitting one
    class across two groups. The group-constant guard cannot survive that — a scoring agent saw
    four constants reported for a group of three chassis.
    """

    def test_both_spellings_of_a_two_word_class_agree(self):
        from scoring import _primary_class
        self.assertEqual(_primary_class("Blood Hunter 17 (Order of the Lycan) / Bard 3"),
                         _primary_class("Bloodhunter 14 (Order of the Mutant) / Bard 6"))

    def test_the_primary_is_the_class_with_the_most_levels(self):
        from scoring import _primary_class
        self.assertEqual(_primary_class("Fighter 11 (Echo Knight) / Paladin 3 / Wizard 6"),
                         "fighter")
        self.assertEqual(
            _primary_class("Ranger 15 (Snowlight Conclave) / Monk 3 (Way of the Friar) "
                           "/ Cleric 2 (Light)"), "ranger")

    def test_a_subclass_parenthetical_is_not_read_as_a_class(self):
        """`(Order of the Lycan)` contains no number, but `Cleric 2 (Light)` must not lose to it."""
        from scoring import _primary_class
        self.assertEqual(_primary_class("Cleric 14 (Tempest) / Bard 6 (College of Stormcalling)"),
                         "cleric")


if __name__ == "__main__":
    unittest.main()
