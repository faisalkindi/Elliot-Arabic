#!/usr/bin/env python3
"""
93_enrich_context.py — decode the structured FText keys into per-line context and
(1) rewrite 01_extracted_strings.jsonl with new fields, (2) emit an ORDERED dialogue
script grouped by chapter/scene for coherent, in-context localization.

Key grammar observed (examples):
  M01_E01_1000_M010_PCM000_m   chapter M01, event E01, block 1000, line M010, speaker PCM000 (player, male)
  M04_E08_1000_M170_NPC1010_00_f  speaker NPC1010, female
  M01_E01_1000_Title           a scene title/heading
  MAGICSTONE_SWORD_08_DESCRIPTION  item text (not dialogue)
  Tutorial_GameStart_03_1_Text     tutorial

New fields added to each record:
  content_type, chapter, scene, block, line_order, speaker, speaker_role, speaker_gender

Run: python 93_enrich_context.py
"""
import json, os, re

HERE = os.path.dirname(__file__)
SRC = os.path.join(HERE, "..", "01_extracted_strings.jsonl")
rows = [json.loads(l) for l in open(SRC, encoding="utf-8")]

SPEAKER = re.compile(r"(PCM\d{3}|PCF\d{3}|NPC\d{3,4})")
GENDER = re.compile(r"_([mf])$")
CHAP = re.compile(r"M(\d{2})_E(\d+)")
BLOCK = re.compile(r"_E\d+_(\d{3,4})")
LINE = re.compile(r"_\d{3,4}_M(\d{3})")


def parse_key(k):
    role = gender = speaker = chapter = scene = None
    block = line = 0
    mg = GENDER.search(k)
    if mg:
        gender = mg.group(1)
    sp = SPEAKER.findall(k)
    if sp:
        speaker = sp[-1]
        role = "player" if speaker.startswith(("PCM", "PCF")) else "npc"
    mc = CHAP.match(k)
    if mc:
        chapter = "M" + mc.group(1)
        scene = f"M{mc.group(1)}_E{mc.group(2)}"
        mb = BLOCK.search(k)
        if mb:
            block = int(mb.group(1))
        ml = LINE.search(k)
        if ml:
            line = int(ml.group(1))
    # content type
    if scene:
        ctype = "dialogue"
    elif k.startswith("Tutorial"):
        ctype = "tutorial"
    elif re.match(r"(MAGICSTONE|ACCESSORY|ITEM|WEAPON)", k):
        ctype = "item"
    elif re.match(r"S\d|SP|DNG|SCN|TALK|NPC\d", k):
        ctype = "dialogue"  # side/non-mainline talk
    else:
        ctype = None
    return dict(content_type=ctype, chapter=chapter, scene=scene, block=block,
                line_order=line, speaker=speaker, speaker_role=role, speaker_gender=gender)


# --- enrich + rewrite 01 ---
for r in rows:
    info = parse_key(r["ftext_key"])
    r.update(info)

with open(SRC, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

# --- ordered main-story dialogue script ---
dlg = [r for r in rows if r.get("scene")]
dlg.sort(key=lambda r: (r["chapter"], r["scene"], r["block"], r["line_order"], r["ftext_key"]))

GARB = re.compile(r"[Ã-ÿ]{2,}")
out = os.path.join(HERE, "..", "dialogue_scenes.md")
with open(out, "w", encoding="utf-8") as f:
    f.write("# Ordered main-story dialogue (chapters M01–M06)\n")
    f.write("Speaker IDs: PCM000 = player (Elliot); NPC#### = NPC. Gender from key (_m/_f).\n")
    f.write("Use this for scene context + Arabic gender agreement. JA source, untranslated.\n\n")
    cur = None
    for r in dlg:
        if r["scene"] != cur:
            cur = r["scene"]
            f.write(f"\n## {cur}\n")
        if GARB.search(r["original_text"]):
            continue
        spk = r["speaker"] or "—"
        g = r["speaker_gender"] or "?"
        txt = r["original_text"].replace("\n", " / ")
        f.write(f"- `{spk}/{g}` {txt}\n")

# stats
from collections import Counter
ct = Counter(r["content_type"] for r in rows)
gen = Counter(r["speaker_gender"] for r in rows if r["speaker_gender"])
spk = Counter(r["speaker"] for r in rows if r["speaker"])
print("enriched 01 with: content_type, chapter, scene, block, line_order, speaker, speaker_role, speaker_gender")
print("content_type:", dict(ct))
print("gender-tagged lines:", dict(gen))
print("lines with speaker id:", sum(spk.values()), "| distinct speakers:", len(spk))
print("main-story ordered dialogue lines:", len(dlg))
print("wrote ->", out)
