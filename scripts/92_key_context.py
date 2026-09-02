#!/usr/bin/env python3
"""
92_key_context.py — analyze the structured FText keys to see what per-line context
(speaker, gender, chapter/scene, content type) we can derive for the translator.
Read-only.
"""
import json, os, re
from collections import Counter

HERE = os.path.dirname(__file__)
rows = [json.loads(l) for l in open(os.path.join(HERE, "..", "01_extracted_strings.jsonl"), encoding="utf-8")]
keys = [r["ftext_key"] for r in rows]
n = len(keys)

hex32 = sum(1 for k in keys if re.fullmatch(r"[0-9A-Fa-f]{32}", k))
print(f"total {n} | opaque 32-hex {hex32} | readable structured {n - hex32}")

# speaker-gender suffix _m / _f (optionally followed by more)
gender = Counter()
for k in keys:
    m = re.search(r"_([mf])$", k)
    if m:
        gender[m.group(1)] += 1
print(f"gender-tagged dialogue keys (_m/_f): {dict(gender)}  total={sum(gender.values())}")

# chapter/scene M##_E##
scene = sum(1 for k in keys if re.match(r"M\d{2}_E\d", k))
chapters = Counter(re.match(r"M(\d{2})_", k).group(1) for k in keys if re.match(r"M\d{2}_E\d", k))
print(f"dialogue keys with M##_E## scene structure: {scene} | chapters: {sorted(chapters)}")
print(f"  per-chapter line counts: {dict(sorted(chapters.items()))}")

# speaker NPC ids
npc = Counter()
for k in keys:
    m = re.search(r"NPC(\d{3,4})", k)
    if m:
        npc[m.group(1)] += 1
print(f"keys with NPC#### speaker id: {sum(npc.values())} | distinct speakers: {len(npc)}")
print(f"  top speakers: {dict(npc.most_common(10))}")

# readable-key prefixes (content type)
pref = Counter(k.split("_")[0] for k in keys if not re.fullmatch(r"[0-9A-Fa-f]{32}", k))
print(f"top readable prefixes (content type): {dict(pref.most_common(20))}")

# sample dialogue scene keys (sorted = scene order)
dlg = sorted(k for k in keys if re.match(r"M\d{2}_E\d", k))
print("sample dialogue keys in scene order:")
for k in dlg[:12]:
    print("   ", k)
