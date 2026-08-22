"""`enumerate_splits --only` must be able to name every subclass in the inventory.

Three headings carry commas, so the comma-joined form cannot address them: it splits one real key
into two keys that match nothing, and `--only` narrows silently rather than failing. `@file` is the
form that can, and it is the form `seed_index.py --scored` already established.
"""
import json, os, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "skills", "listo-ledger")
sys.path.insert(0, os.path.join(LEDGER, "scripts"))
import enumerate_splits as ES  # noqa: E402


def comma_keys():
    """Comma-bearing subclass keys, read from the real base profiles.

    Read-only, and deliberately not a frozen fixture: a hand-copied list would keep passing after
    the headings it names stop existing, which is the opposite of what this test is for.
    """
    with open(os.path.join(LEDGER, "assets", "subclass-bases.json")) as fh:
        doc = json.load(fh)
    bases = doc.get("bases", doc)
    return sorted(k for k in bases if "," in k)


class OnlyKeys(unittest.TestCase):

    def test_none_means_every_key(self):
        self.assertIsNone(ES.only_keys(None))
        self.assertIsNone(ES.only_keys(""))

    def test_comma_form_still_works(self):
        self.assertEqual(ES.only_keys("cleric/Tempest,wizard/Evocation"),
                         {"cleric/Tempest", "wizard/Evocation"})

    def test_comma_bearing_key_survives_at_file(self):
        keys = comma_keys()
        self.assertTrue(keys, "no comma-bearing subclass key in the inventory — "
                              "if that is now true, this test has nothing left to prove")
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "work-list")
            with open(path, "w") as fh:
                fh.write("\n".join(keys) + "\n")
            self.assertEqual(ES.only_keys("@" + path), set(keys))

    def test_comma_form_cannot_express_them(self):
        """The defect itself, pinned: this is why `@file` had to exist."""
        keys = comma_keys()
        self.assertNotEqual(ES.only_keys(",".join(keys)), set(keys))

    def test_at_file_ignores_blank_lines_and_whitespace(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "work-list")
            with open(path, "w") as fh:
                fh.write("  cleric/Tempest  \n\n\twizard/Evocation\n\n")
            self.assertEqual(ES.only_keys("@" + path),
                             {"cleric/Tempest", "wizard/Evocation"})


if __name__ == "__main__":
    unittest.main()
