#!/usr/bin/env python3
"""
91_analyze_japanese.py — mine the extracted Japanese strings to ground game context
(04) and glossary candidates (05). Read-only analysis of 01_extracted_strings.jsonl.

Outputs to stdout:
  - katakana proper-noun candidates (names/places/loanwords) by frequency
  - frequent short labels (UI/system)
  - longest strings (dialogue/lore samples)
  - rich-text tag inventory

Run: python 91_analyze_japanese.py
"""
import json, os, re
from collections import Counter

HERE = os.path.dirname(__file__)
ROWS = [json.loads(l) for l in open(os.path.join(HERE, "..", "01_extracted_strings.jsonl"), encoding="utf-8")]

KATAKANA_RUN = re.compile(r"[ァ-ヶー]{2,}")          # katakana words (names/loanwords)
TAG = re.compile(r"<[^>]+>")
CJK = re.compile(r"[぀-ヿ㐀-鿿]")
GARBLED = re.compile(r"[Ã-ÿ]{2,}")

clean = [r for r in ROWS if not GARBLED.search(r["original_text"])]
print(f"rows: {len(ROWS)}  (clean, non-mojibake: {len(clean)})\n")

# 1) katakana proper-noun candidates
kata = Counter()
for r in clean:
    for m in KATAKANA_RUN.findall(r["original_text"]):
        if len(m) >= 2:
            kata[m] += 1
print("=== Top katakana terms (names / places / loanwords — glossary candidates) ===")
for term, c in kata.most_common(50):
    print(f"  {c:5d}  {term}")

# 2) frequent short labels (likely UI / system / category)
short = Counter()
for r in clean:
    t = TAG.sub("", r["original_text"]).strip()
    if 1 <= len(t) <= 8 and CJK.search(t):
        short[t] += 1
print("\n=== Frequent short labels (UI/system/menu candidates) ===")
for term, c in short.most_common(40):
    print(f"  {c:5d}  {term}")

# 3) rich-text tag inventory (must be preserved verbatim)
tags = Counter()
for r in ROWS:
    for m in TAG.findall(r["original_text"]):
        tags[m] += 1
print("\n=== Rich-text / markup tags present (PRESERVE verbatim) ===")
for term, c in tags.most_common(30):
    print(f"  {c:5d}  {term}")

# 4) longest strings = dialogue / lore samples
longest = sorted(clean, key=lambda r: len(r["original_text"]), reverse=True)[:8]
print("\n=== Longest strings (dialogue / lore samples) ===")
for r in longest:
    t = r["original_text"].replace("\n", " / ")
    print(f"  [{len(r['original_text'])}] {t[:160]}")
