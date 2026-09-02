#!/usr/bin/env python3
"""
98_fix_contaminated_sources.py — fix 01 rows whose original_text absorbed adjacent
content during the earlier multi-line CSV parse (signature: a REAL newline char, chr 10,
in the source — legit line breaks use the literal `\n` token, not a real newline).
Truncates each at the first real newline. Reports the changed IDs (= re-translate list).
"""
import json, os, shutil

HERE = os.path.dirname(__file__)
P = os.path.join(HERE, "..", "01_extracted_strings.jsonl")
bak = P + ".precontam.bak"
if not os.path.exists(bak):
    shutil.copy2(P, bak)

recs = [json.loads(l) for l in open(P, encoding="utf-8")]
changed = []
for r in recs:
    t = r["original_text"]
    if "\n" in t or "\r" in t:           # real newline char => contamination
        clean = t.split("\n")[0].split("\r")[0]
        if clean != t:
            changed.append((r["id"], t[:60], clean[:60]))
            r["original_text"] = clean

with open(P, "w", encoding="utf-8") as f:
    for r in recs:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"contaminated sources fixed: {len(changed)}")
for cid, before, after in changed:
    print(f"  {cid}\n    before: {before!r}\n    after : {after!r}")
# write re-translate list
with open(os.path.join(HERE, "..", "_retranslate_contaminated.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(c[0] for c in changed))
print(f"\nre-translate list -> _retranslate_contaminated.txt ({len(changed)} ids)")
