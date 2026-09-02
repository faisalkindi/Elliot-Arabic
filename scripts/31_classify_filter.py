#!/usr/bin/env python3
"""
31_classify_filter.py — split 01_extracted_strings.jsonl into:
  - keeps high/medium player-facing rows in 01 (untouched; this script is non-destructive)
  - ../02_uncertain_strings.csv          (confidence == low, or category == unknown)
  - ../03_non_translatable_candidates.csv (debug/path/enum/number-only, with reason)

NOTHING is deleted. Rows can appear in 02/03 as *candidates* for human review.

Usage: python 31_classify_filter.py
"""
import json, os, csv, re

DEBUG_RX   = re.compile(r"\b(DEBUG|TODO|PLACEHOLDER|TEST|TEMP|Lorem|XXX|FIXME|dummy)\b", re.I)
PATH_RX    = re.compile(r"^/(Game|Engine|Script)/|\.(uasset|umap|png|wav|mp3|ono|bin)$", re.I)
ENUM_RX    = re.compile(r"^E[A-Z][A-Za-z0-9_]*$|^[A-Z][A-Z0-9_]{2,}$")
NUMERIC_RX = re.compile(r"^[\d\s.,:%/+\-]+$")
GUID_RX    = re.compile(r"^[A-F0-9]{16,}$", re.I)


def non_translatable_reason(text):
    t = text.strip()
    if DEBUG_RX.search(t):   return "debug/placeholder marker"
    if PATH_RX.search(t):    return "asset path / filename"
    if GUID_RX.match(t):     return "GUID/hash"
    if NUMERIC_RX.match(t):  return "numeric/symbols only"
    if ENUM_RX.match(t):     return "enum/identifier token"
    if len(t) == 1:          return "single character"
    return None


def main():
    here = os.path.dirname(__file__)
    cfg = json.load(open(os.path.join(here, "config.json"), encoding="utf-8"))
    base = os.path.join(here, cfg["out_dir"])
    src = os.path.join(base, "01_extracted_strings.jsonl")
    if not os.path.exists(src):
        print("01_extracted_strings.jsonl not found; run 30_build_extracted.py first.")
        return

    uncertain, nontrans = [], []
    for line in open(src, encoding="utf-8"):
        r = json.loads(line)
        text = r["original_text"]
        reason = non_translatable_reason(text)
        if reason:
            nontrans.append((r["id"], r["source_file"], r["locator"], text, reason))
        elif r["confidence"] == "low" or r["category"] == "unknown":
            nontrans_reason = "low confidence" if r["confidence"] == "low" else "uncategorized"
            uncertain.append((r["id"], r["source_file"], r["locator"], text,
                              r["category"], r["confidence"], nontrans_reason))

    with open(os.path.join(base, "02_uncertain_strings.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "source_file", "locator", "original_text", "category", "confidence", "why_uncertain"])
        w.writerows(uncertain)

    with open(os.path.join(base, "03_non_translatable_candidates.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "source_file", "locator", "original_text", "reason"])
        w.writerows(nontrans)

    print(f"02_uncertain_strings.csv: {len(uncertain)} rows")
    print(f"03_non_translatable_candidates.csv: {len(nontrans)} rows")
    print("(01 left intact — nothing deleted.)")


if __name__ == "__main__":
    main()
