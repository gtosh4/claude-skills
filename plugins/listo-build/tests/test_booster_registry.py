"""The booster registry is closed, and the documents that quote it must quote all of it.

`scoring.BOOSTERS` is the registry. `ledger-schema.md` and `grants-brief.md` each carry a table of
it, and the briefs are what an authoring pass actually reads — `base-brief.md`'s read set does not
include the schema, so for the tier-1 pass `grants-brief.md` **is** the registry.

Seven ids drifted out of that copy: `indomitable`, `supernatural-defense`, `cosmic-omen`,
`legendary-resistance`, `soul-of-artifice`, `danger-sense` and `bladesong`. All seven were found by
the tier-1 grants pass and added to the code and the schema, and none was written back into the
brief that pass reads. A live run then reported Fighter's Indomitable as having no id at all and
left it off all fourteen fighters.

That is the omission the fail-closed doctrine cannot catch. An *unknown* id raises; an id the
author never knew existed scores as nothing, and a score that is too low reads exactly like an
honest one.
"""
import os, re, sys, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "skills", "listo-ledger")
sys.path.insert(0, os.path.join(ROOT, "skills", "listo-build", "scripts"))
from scoring import BOOSTERS  # noqa: E402

# Every document that reproduces the registry, and who reads it.
QUOTED_IN = {
    "ledger-schema.md": "the scoring pass's authority on the output shape",
    "grants-brief.md": "the tier-1 base pass's only view of the registry",
}


def documented(name):
    """The ids in the document's booster table.

    Scoped to the one table whose header is `| id | what | scope`, because both files carry other
    backticked-first-column tables — redirect ids, chassis fields — and a document-wide sweep reads
    those as boosters.
    """
    with open(os.path.join(LEDGER, "assets", name)) as fh:
        lines = fh.read().split("\n")
    out, inside = set(), False
    for line in lines:
        if line.startswith("| id | what | scope"):
            inside = True
        elif inside:
            m = re.match(r"^\| `([a-z-]+)` \|", line)
            if m:
                out.add(m.group(1))
            elif not line.startswith("|"):
                inside = False
    return out


class Registry(unittest.TestCase):

    def test_every_document_names_every_booster(self):
        for name, who in QUOTED_IN.items():
            with self.subTest(document=name):
                missing = sorted(set(BOOSTERS) - documented(name))
                self.assertEqual(missing, [], f"{name} is {who}, and omits {missing}")

    def test_no_document_names_a_booster_the_registry_lacks(self):
        """The other direction: a documented id nothing implements would raise on first use."""
        for name in QUOTED_IN:
            with self.subTest(document=name):
                extra = sorted(documented(name) - set(BOOSTERS))
                self.assertEqual(extra, [], f"{name} names {extra}, which `BOOSTERS` does not")


if __name__ == "__main__":
    unittest.main()
