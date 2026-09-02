#!/usr/bin/env python3
"""
97_normalize_translation.py — standing post-batch normalizer for 10_arabic_translation.jsonl.

Fixes line-break token representation so it matches the game's literal `\n` token:
  - un-doubles over-escaped newline tokens  (backslash backslash n  ->  backslash n)
  - converts any real CR/LF chars back to the `\n` token
Idempotent. Run after every batch, before QA. Rewrites 10 in place (backup kept once).
"""
import json, os, shutil

HERE = os.path.dirname(__file__)
P = os.path.join(HERE, "..", "10_arabic_translation.jsonl")
bak = P + ".bak"
if not os.path.exists(bak):
    shutil.copy2(P, bak)

recs = [json.loads(l) for l in open(P, encoding="utf-8") if l.strip()]
fixed = 0
for r in recs:
    a = r.get("arabic", "")
    orig = a
    # 1) un-double escaped newline token:  "\\n" (2 backslashes + n) -> "\n" (1 backslash + n)
    a = a.replace("\\\\n", "\\n")
    # 2) real newline chars -> the literal token
    a = a.replace("\r\n", "\\n").replace("\r", "\\n").replace("\n", "\\n")
    if a != orig:
        r["arabic"] = a
        fixed += 1

with open(P, "w", encoding="utf-8") as f:
    for r in recs:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"normalized {fixed} rows (newline tokens) of {len(recs)} | backup: {os.path.basename(bak)}")
