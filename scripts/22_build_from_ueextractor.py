#!/usr/bin/env python3
"""
22_build_from_ueextractor.py — turn UEExtractor's locresCSV into the workspace outputs.

Input : UEExtractor `key,source,Translation` CSV (deduped by FText key).
        Default: scripts/_tools/UEExtractor/Paks_locres_commas.csv
Output: ../01_extracted_strings.jsonl, ../02_uncertain_strings.csv,
        ../03_non_translatable_candidates.csv

The FText key (32-hex) is UE's stable identifier and serves as the trace key for
re-injection. Source language is Japanese (the game's native text).

Run: python 22_build_from_ueextractor.py [path_to_csv]
"""
import sys, os, re, json, csv
from collections import Counter
from placeholder_spec import extract_tokens

# A record line is "<key>,<source>,"  (Translation empty -> trailing comma).
# Key is an ASCII identifier or 32-hex hash (no comma, no spaces, no CJK).
REC_RE = re.compile(r"^([^,\r\n]+),(.*),$")
KEYLIKE = re.compile(r"^[A-Za-z0-9_.\-/\[\]#]+$")
CJK = re.compile(r"[぀-ヿ㐀-鿿ｦ-ﾟ]")
MOJIBAKE = re.compile(r"[-ÿ]")


def recover_mojibake(s):
    """Some FText came out as UTF-8 bytes mis-decoded as Latin-1. If re-decoding
    latin-1 -> utf-8 yields CJK, it's the real text. Returns (text, recovered?)."""
    if not s or not MOJIBAKE.search(s) or CJK.search(s):
        return s, False
    try:
        fixed = s.encode("latin-1", "strict").decode("utf-8", "strict")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s, False
    if CJK.search(fixed) or fixed.count("�") == 0 and fixed != s and any(ord(c) > 0x2000 for c in fixed):
        return fixed, True
    return s, False
GARBAGE = re.compile(r"[�\x00-\x08\x0e-\x1f]")          # replacement char / control bytes
DEBUG_RE = re.compile(r"\b(Tips?:|DEBUG|TODO|PLACEHOLDER|debug|material|outline of the blur)\b")
ALLCAPS_ID = re.compile(r"^[A-Z0-9_]+$")

CATEGORY_HINTS = [
    ("skill_description", re.compile(r"(ダメージ|攻撃|防御|回復|効果|付与|発動|スキル|アビリティ)")),
    ("item_description",  re.compile(r"(アイテム|装備|武器|防具|まもり|魔石|ませき|道具|入手|消費)")),
    ("system_message",    re.compile(r"(してください|できません|ますか|しますか|保存|セーブ|ロード|エラー|確認)")),
    ("menu",              re.compile(r"(設定|オプション|メニュー|タイトル|音量|言語|画面|操作)")),
    ("tutorial",          re.compile(r"(チュートリアル|操作方法|ヒント|遊び方)")),
    ("ui",                re.compile(r"(マップ|スコア|レベル|ＨＰ|HP|MP|ゴールド|所持|一覧)")),
]


def read_records(path):
    """Yield (key, source) for every record (hex OR readable keys). Lines that don't
    start a new record are treated as continuations of a multi-line source."""
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    cur = None
    for ln in lines:
        ln = ln.rstrip("\r")
        m = REC_RE.match(ln)
        if m and KEYLIKE.match(m.group(1)) and m.group(1).lower() != "key":
            if cur is not None:
                yield cur[0], cur[1]
            cur = [m.group(1), m.group(2)]
        elif cur is not None:
            cur[1] += "\n" + ln
    if cur is not None:
        yield cur[0], cur[1]


def classify_noise(src):
    if not src.strip():
        return "empty"
    g = len(GARBAGE.findall(src))
    if g >= 3 or (len(src) > 0 and g / len(src) > 0.05):
        return "binary/garbage"
    if DEBUG_RE.search(src):
        return "debug/dev string"
    if ALLCAPS_ID.match(src) and len(src) > 1 and " " not in src:
        return "identifier/enum token"
    if re.fullmatch(r"[\d\s.,:%/+\-]+", src):
        return "numeric/symbols only"
    return None


def category(src):
    """Step-2 classification into the brief's text types. Highest-precision signal first."""
    s = src
    plain = re.sub(r"<[^>]+>", "", s).strip()
    if "<btn" in s and re.search(r"操作|長押し|押そう|押す|ボタン|変更|表示|できる|しよう", s):
        return "tutorial"
    if re.search(r"チュートリアル|操作方法|遊び方|ヒント|『システム|短く押|長押し", s):
        return "tutorial"
    if re.search(r"設定|オプション|垂直同期|コントローラー|音量|画面効果|言語|解像度|明るさ|"
                 r"タイトルへ戻る|閉じる|決定|キャンセル|もどる|戻る$|はい$|いいえ$|オン$|オフ$|最高$", s):
        return "menu"
    if re.search(r"してください|できません|ください。?$|ますか[。？]?$|しますか|"
                 r"セーブ|ロード|オートセーブ|データ|上書き|よろしいですか|保存", s):
        return "system_message"
    if "RI_ICON_WPN" in s or re.search(r"魔石|ませき|装備|武具|防具|まもり|道具|入手|消費|レシピ|素材", s):
        return "item_description" if len(plain) > 8 else "item_name"
    if re.search(r"ダメージ|攻撃力|防御力|与える|効果|付与|発動|スキル|アビリティ|チャージ|"
                 r"クリティカル|回復|耐久|ステータス|バフ", s):
        return "skill_description" if len(plain) > 8 else "skill_name"
    if re.search(r"クエスト|依頼|任務|目標|報酬", s):
        return "quest_description" if len(plain) > 12 else "quest_title"
    if CJK.search(s) and (re.search(r"[。！？…♪」』]", s) or len(plain) > 22):
        return "dialogue"
    if 1 <= len(plain) <= 10:
        return "ui"
    if not CJK.search(s):
        return "ui"
    return "unknown"


def confidence(src):
    if classify_noise(src):
        return "low"
    if CJK.search(src) or len(src.split()) > 1:
        return "high"
    return "medium"


def main():
    here = os.path.dirname(__file__)
    csv_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        here, "_tools", "UEExtractor", "Paks_locres_commas.csv")
    base = os.path.join(here, "..")
    if not os.path.exists(csv_path):
        print(f"CSV not found: {csv_path}"); return

    rows, uncertain, nontrans = [], [], []
    cats, confs = Counter(), Counter()
    seen = set()
    recovered_n = 0
    for key, src in read_records(csv_path):
        if key in seen:
            continue
        seen.add(key)
        src, rec_fixed = recover_mojibake(src)
        if rec_fixed:
            recovered_n += 1
        toks = extract_tokens(src)
        noise = classify_noise(src)
        cat = category(src)
        conf = confidence(src)
        cats[cat] += 1; confs[conf] += 1
        rec = {
            "id": "EL_" + key,
            "ftext_key": key,
            "source_lang": "ja",
            "original_text": src,
            "category": cat,
            "placeholders": toks,
            "placeholder_notes": ("none" if not toks else f"PRESERVE: {toks}"),
            "confidence": conf,
            "context": None,
        }
        rows.append(rec)
        if noise:
            nontrans.append((rec["id"], key, src[:120], noise))
        elif conf == "low" or cat == "unknown":
            uncertain.append((rec["id"], key, src[:160], cat, conf))

    with open(os.path.join(base, "01_extracted_strings.jsonl"), "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(os.path.join(base, "02_uncertain_strings.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f); w.writerow(["id", "ftext_key", "original_text", "category", "confidence"])
        w.writerows(uncertain)
    with open(os.path.join(base, "03_non_translatable_candidates.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f); w.writerow(["id", "ftext_key", "original_text", "reason"])
        w.writerows(nontrans)

    print(f"Total unique strings: {len(rows)}")
    print(f"  -> 01_extracted_strings.jsonl")
    print(f"  -> 02_uncertain_strings.csv ({len(uncertain)})")
    print(f"  -> 03_non_translatable_candidates.csv ({len(nontrans)})")
    print(f"categories: {dict(cats)}")
    print(f"confidence: {dict(confs)}")
    jp = sum(1 for r in rows if CJK.search(r['original_text']))
    print(f"language: japanese={jp}  non-japanese={len(rows)-jp}")
    withtok = sum(1 for r in rows if r['placeholders'])
    print(f"strings with placeholders/tags: {withtok}")
    print(f"mojibake recovered: {recovered_n}")


if __name__ == "__main__":
    main()
