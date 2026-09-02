#!/usr/bin/env python3
"""
30_build_extracted.py — merge parsed rows -> ../01_extracted_strings.jsonl

Combines _rows_locres.jsonl + _rows_datatable.jsonl, assigns stable unique IDs,
does a FIRST-PASS heuristic category guess, records placeholders, and sets a
confidence level. Human/agent review refines categories afterward.

Confidence:
  high   - clear player text from .locres or an FText SourceString, has letters, has spaces
  medium - DataTable bare-string leaf, or short single word
  low    - all-caps/identifier-ish, very short, or no spaces

Usage: python 30_build_extracted.py
"""
import json, os, glob, re, hashlib
from placeholder_spec import extract_tokens

CATEGORY_HINTS = [
    ("item_description", re.compile(r"(Item|Equip|Weapon|Armor|Accessory).*Desc|Desc.*Item", re.I)),
    ("item_name",        re.compile(r"(Item|Equip|Weapon|Armor|Accessory).*Name|ItemDB", re.I)),
    ("skill_description", re.compile(r"(Skill|Ability|Magic|Art).*Desc", re.I)),
    ("skill_name",       re.compile(r"(Skill|Ability|Magic|Art).*Name|AbilityData", re.I)),
    ("quest_title",      re.compile(r"Quest.*(Title|Name)", re.I)),
    ("quest_description", re.compile(r"Quest.*Desc", re.I)),
    ("tutorial",         re.compile(r"Tutorial|Help|Guide", re.I)),
    ("achievement",      re.compile(r"Achieve|Trophy", re.I)),
    ("system_message",   re.compile(r"System|Message|Notify|Error|Confirm|Dialog", re.I)),
    ("menu",             re.compile(r"Menu|Title|Option|Setting|Config", re.I)),
    ("ui",               re.compile(r"UI|HUD|Window|Button|Label|WBP|Widget", re.I)),
    ("dialogue",         re.compile(r"Talk|Dialog|Script|Story|Event|Serif|Message", re.I)),
    ("lore",             re.compile(r"Lore|Glossary|Encyclo|Library|History", re.I)),
]


def guess_category(blob):
    for cat, rx in CATEGORY_HINTS:
        if rx.search(blob):
            return cat
    return "unknown"


def mk_id(source_file, locator, text):
    base = f"{os.path.basename(source_file)}|{locator}|{text}"
    return "EL_" + hashlib.sha1(base.encode("utf-8")).hexdigest()[:12].upper()


def confidence(text, from_locres, locator):
    t = text.strip()
    if len(t) <= 2 or re.match(r"^[A-Z0-9_]+$", t):
        return "low"
    if from_locres or " " in t:
        return "high"
    return "medium"


def main():
    here = os.path.dirname(__file__)
    cfg = json.load(open(os.path.join(here, "config.json"), encoding="utf-8"))
    ext = os.path.join(here, cfg["work_extract"])
    out_path = os.path.join(here, cfg["out_dir"], "01_extracted_strings.jsonl")

    rows, seen = [], set()

    def add(source_file, locator, text, ns, key, from_locres):
        if not text or not text.strip():
            return
        rid = mk_id(source_file, locator, text)
        if rid in seen:
            return
        seen.add(rid)
        blob = f"{source_file} {locator} {ns or ''} {key or ''}"
        toks = extract_tokens(text)
        rows.append({
            "id": rid,
            "source_file": source_file,
            "locator": locator,            # namespace/key or key_path
            "ue_namespace": ns,
            "ue_key": key,
            "original_text": text,
            "category": guess_category(blob),
            "context": None,               # filled during review / from neighbouring rows
            "placeholders": toks,
            "placeholder_notes": ("none" if not toks else f"PRESERVE: {toks}"),
            "confidence": confidence(text, from_locres, locator),
        })

    lp = os.path.join(ext, "_rows_locres.jsonl")
    if os.path.exists(lp):
        for line in open(lp, encoding="utf-8"):
            r = json.loads(line)
            add(r["source_file"], f"{r['namespace']}/{r['key']}",
                r["original_text"], r["namespace"], r["key"], True)

    dp = os.path.join(ext, "_rows_datatable.jsonl")
    if os.path.exists(dp):
        for line in open(dp, encoding="utf-8"):
            r = json.loads(line)
            add(r["source_file"], r["key_path"], r["original_text"],
                r.get("ue_namespace"), r.get("ue_key"), False)

    if not rows:
        print("Nothing to build. Run 20_/21_ parsers first.")
        return

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    from collections import Counter
    cats = Counter(r["category"] for r in rows)
    conf = Counter(r["confidence"] for r in rows)
    print(f"Wrote {len(rows)} unique strings -> {out_path}")
    print("  categories:", dict(cats))
    print("  confidence:", dict(conf))


if __name__ == "__main__":
    main()
