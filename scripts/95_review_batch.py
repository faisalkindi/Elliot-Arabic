#!/usr/bin/env python3
"""
95_review_batch.py — review a returned translation batch:
1. coverage vs the intended category set (default: ui+menu)
2. build a joined CSV (ID, source text, Arabic translation, category, notes) for 40_qa_validate.py

Usage: python 95_review_batch.py [category ...]   (default: ui menu)
"""
import json, os, csv, sys
from collections import Counter

HERE = os.path.dirname(__file__)
BASE = os.path.join(HERE, "..")
cats = sys.argv[1:] or ["ui", "menu"]

src = {r["id"]: r for r in (json.loads(l) for l in open(os.path.join(BASE, "01_extracted_strings.jsonl"), encoding="utf-8"))}
skip = set(r["id"] for r in csv.DictReader(open(os.path.join(BASE, "03_non_translatable_candidates.csv"), encoding="utf-8-sig")))
tr = {r["id"]: r for r in (json.loads(l) for l in open(os.path.join(BASE, "10_arabic_translation.jsonl"), encoding="utf-8") if l.strip())}

# intended set: rows in those categories, excluding 03
intended = {i for i, r in src.items() if r["category"] in cats and i not in skip}
covered = intended & set(tr)
missing = intended - set(tr)
extra = set(tr) - set(src)  # ids not in source at all

print(f"intended ({'+'.join(cats)}, excl 03): {len(intended)}")
print(f"  covered: {len(covered)}  | MISSING: {len(missing)}")
print(f"translation records total: {len(tr)}")
print(f"  ids not found in source 01: {len(extra)}")
# category breakdown of what was actually translated
trcats = Counter(src[i]["category"] for i in tr if i in src)
print("translated-by-category:", dict(trcats))
if missing:
    print("\nsample MISSING ids (untranslated in this batch):")
    for i in list(missing)[:15]:
        print("   ", i, "|", src[i]["original_text"][:50])

# build joined QA csv
out = os.path.join(BASE, "_qa_batch_join.csv")
with open(out, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ID", "source text", "Arabic translation", "category", "notes"])
    for i, t in tr.items():
        s = src.get(i, {})
        w.writerow([i, s.get("original_text", ""), t.get("arabic", ""), s.get("category", ""), t.get("notes", "")])
print(f"\nwrote QA join -> {out}")
