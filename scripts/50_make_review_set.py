#!/usr/bin/env python3
"""
50_make_review_set.py — build an independent-review set for a translated batch.
Pairs each translated line with its Japanese source + speaker/gender so a FRESH
reviewer (a separate subagent, or another model) can back-translate and judge
meaning fidelity, gender agreement, register, and glossary use.

Usage:
  python 50_make_review_set.py [--n 40] [--category dialogue] [--seed-index 0]
Writes: ../_review_set.md  (human/agent-readable)  and  ../_review_set.jsonl
"""
import json, os, csv, argparse

HERE = os.path.dirname(__file__)
BASE = os.path.join(HERE, "..")


def load():
    src = {r["id"]: r for r in (json.loads(l) for l in open(os.path.join(BASE, "01_extracted_strings.jsonl"), encoding="utf-8"))}
    tr = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(BASE, "10_arabic_translation.jsonl"), encoding="utf-8") if l.strip()}
    return src, tr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--category", default=None)
    ap.add_argument("--seed-index", type=int, default=0, help="deterministic stride start (no RNG, resume-safe)")
    a = ap.parse_args()
    src, tr = load()

    pool = [i for i in tr if i in src and (a.category is None or src[i]["category"] == a.category)]
    pool.sort()
    # deterministic even spread across the pool (so different runs cover different rows)
    if pool:
        stride = max(1, len(pool) // a.n)
        picked = pool[a.seed_index::stride][:a.n]
    else:
        picked = []

    rows = []
    for i in picked:
        s, t = src[i], tr[i]
        rows.append({
            "id": i, "category": s["category"], "speaker": s.get("speaker"),
            "speaker_gender": s.get("speaker_gender"), "scene": s.get("scene"),
            "source_ja": s["original_text"], "arabic": t.get("arabic", ""),
        })

    with open(os.path.join(BASE, "_review_set.jsonl"), "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    with open(os.path.join(BASE, "_review_set.md"), "w", encoding="utf-8") as f:
        f.write(f"# Independent review set — {len(rows)} lines\n\n")
        for r in rows:
            sp = f"{r['speaker'] or '—'}/{r['speaker_gender'] or '?'}"
            f.write(f"- **{r['id']}**  ({r['category']}, speaker {sp})\n")
            f.write(f"  - JA: {r['source_ja']}\n")
            f.write(f"  - AR: {r['arabic']}\n\n")
    print(f"review set: {len(rows)} lines -> _review_set.md / _review_set.jsonl")


if __name__ == "__main__":
    main()
