#!/usr/bin/env python3
"""
96_flag_mojibake.py — find corrupt/mojibake source rows in 01 (UTF-16-misread Japanese,
e.g. 'Aÿ­0ã0é0¯0ü0') and append them to 03_non_translatable_candidates.csv so future
batches skip them. Non-destructive: only appends ids not already in 03.
"""
import json, os, csv, re

HERE = os.path.dirname(__file__)
BASE = os.path.join(HERE, "..")
CJK = re.compile(r"[぀-ヿ㐀-鿿ｦ-ﾟ]")
AR = re.compile(r"[؀-ۿ]")


def is_mojibake(s):
    if not s or CJK.search(s) or AR.search(s):
        return False
    weird = sum(1 for c in s if 0x80 <= ord(c) <= 0x24F)          # Latin-1 supp + Latin ext
    # mojibake = several stray non-ASCII Latin chars, or that mixed with many bare digits/symbols
    if weird >= 2:
        return True
    if weird >= 1 and len(re.findall(r"[0-9`~^]", s)) >= 4 and not re.search(r"[A-Za-z]{4,}", s):
        return True
    return False


rows = [json.loads(l) for l in open(os.path.join(BASE, "01_extracted_strings.jsonl"), encoding="utf-8")]
have = set(r["id"] for r in csv.DictReader(open(os.path.join(BASE, "03_non_translatable_candidates.csv"), encoding="utf-8-sig")))
new = [r for r in rows if is_mojibake(r["original_text"]) and r["id"] not in have]

with open(os.path.join(BASE, "03_non_translatable_candidates.csv"), "a", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    for r in new:
        w.writerow([r["id"], r["ftext_key"], r["original_text"][:120], "mojibake/corrupt source"])

print(f"already in 03: {len(have)} | newly flagged mojibake: {len(new)} | 03 total now: {len(have)+len(new)}")
for r in new[:8]:
    print("   ", r["id"], "|", r["original_text"][:40])
