#!/usr/bin/env python3
"""Assign chassis ids centrally, after scoring, so parallel agents cannot collide.

Five agents naming bodies at once cannot see each other's picks. In v3 that produced 8 collisions
and in v4 thirteen — and because the merge was a dict assignment, each collision silently
OVERWROTE a body. Thirteen subclasses then read as uncovered, which is how it was caught; a
smaller run would not have been.

So names are proposed by the agent and *resolved here*, against the whole set at once. The
resolution is deterministic: same input, same ids, every time.
"""
import re

STOP = {"the", "of", "way", "path", "circle", "college", "order", "oath", "school",
        "domain", "aspect", "conclave", "base", "game", "vanilla", "expansion", "ua"}


def _words(text):
    return [w for w in re.split(r"[^A-Za-z]+", text) if w and w.lower() not in STOP]


def candidates(proposed, key):
    """Fallback names for one body, best first: its own proposal, then the subclass's own words."""
    out = [proposed]
    sub = key.split("/", 1)[1] if "/" in key else key
    ws = _words(sub)
    out += ws                                    # Ascendant, Dragon, ...
    out += [a + b.lower() for a, b in zip(ws, ws[1:])]   # AscendantDragon
    cls = key.split("/", 1)[0].title()
    out += [f"{w}{cls}" for w in ws]
    return [w for w in out if w and w[0].isupper()]


def assign(bodies, taken=()):
    """`bodies` is `[(proposed, key)]`. Returns `{index: id}` with every id unique.

    `taken` seeds the set with ids that already exist — an earlier pass's roster — so a later
    pass keeps those names stable and only the new bodies move.

    Order-independent by construction: bodies are resolved in sorted key order, so the same set
    always produces the same assignment regardless of which agent returned first.
    """
    order = sorted(range(len(bodies)), key=lambda i: (bodies[i][1], bodies[i][0]))
    taken, out = set(taken), {}
    for i in order:
        proposed, key = bodies[i]
        for c in candidates(proposed, key):
            if c not in taken:
                taken.add(c)
                out[i] = c
                break
        else:                                     # every candidate taken: number the proposal
            n = 2
            while f"{proposed}{n}" in taken:
                n += 1
            taken.add(f"{proposed}{n}")
            out[i] = f"{proposed}{n}"
    return out
