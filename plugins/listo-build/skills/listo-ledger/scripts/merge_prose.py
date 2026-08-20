#!/usr/bin/env python3
"""Merge rewritten entry prose and self-contained roster notes back into a ledger.

Also enforces the two things the prose keeps getting wrong:

  labels     the template prints "Reads as." and "Costs." itself, so authored prose that opens
             with them renders the label twice. Stripped here as well as at render time, because
             the data should be right and not merely display right.
  standalone a roster note may not require another card to make sense. Cannot be checked
             mechanically — several chassis ids are also real game words — so residual
             cross-references are REPORTED for a human read, never auto-edited.
"""
import json, sys, glob, re, collections

LABELS = (("verdict", "Reads as"), ("cost", "Costs"))


def delabel(text, label):
    t = (text or "").lstrip()
    for opener in (label.lower() + ".", label.lower()):
        if t.lower().startswith(opener):
            return t[len(opener):].lstrip()
    return t


def main(ledger, prosedir, dest=None):
    L = json.load(open(ledger))
    C, E = L["chassis"], L["entries"]

    notes = {}
    for f in sorted(glob.glob(f"{prosedir}/notes_out*.json")):
        notes.update(json.load(open(f)))
    ents = {}
    for f in sorted(glob.glob(f"{prosedir}/entries_out*.json")):
        ents.update(json.load(open(f)))

    unknown = [k for k in list(notes) + list(ents) if k not in C]
    if unknown:
        print(f"! unknown chassis in prose output: {unknown}")
        return 1

    for cid, rec in notes.items():
        if "note" in rec:
            C[cid]["note"] = rec["note"].strip()
    for cid, rec in ents.items():
        e = E.setdefault(cid, {})
        for field in ("tag", "verdict", "cost", "vars"):
            if field in rec:
                e[field] = rec[field]
        for field, label in LABELS:
            if field in e:
                e[field] = delabel(e[field], label)
        e.pop("name", None)      # derived from the pairing; authoring it is a hard error
    print(f"applied {len(notes)} roster notes, {len(ents)} entries")

    # residual cross-references, for a human read
    ids = set(C)
    resid = collections.defaultdict(list)
    for cid, c in C.items():
        for other in ids - {cid}:
            if re.search(rf"\b{re.escape(other)}\b", c.get("note", "")):
                resid[cid].append(other)
    print(f"\n{len(resid)} roster notes still name another chassis id "
          f"(many are game words, not references — read before acting):")
    for cid, others in sorted(resid.items())[:12]:
        print(f"    {cid}: {others}")

    json.dump(L, open(dest or ledger, "w"), indent=2, ensure_ascii=False)
    print(f"\nwrote {dest or ledger}")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
