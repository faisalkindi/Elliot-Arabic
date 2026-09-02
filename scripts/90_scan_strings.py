#!/usr/bin/env python3
"""
90_scan_strings.py — DISCOVERY tool. Scan extracted cooked assets for human-readable
text (UTF-16LE and UTF-8 FStrings), to locate WHERE the translatable strings live and
in WHAT encoding, before committing to a parser. Read-only.

Reports: per-folder counts of "interesting" strings (containing Japanese kana/kanji, or
multi-word Latin), and prints samples per top file.

Usage: python 90_scan_strings.py [root]   (default root = ../_extract)
"""
import sys, os, re, struct, glob
from collections import Counter, defaultdict

CJK = re.compile(r"[぀-ヿ㐀-鿿ｦ-ﾟ]")   # kana + kanji + halfwidth kana
LATIN_SENT = re.compile(r"[A-Za-z][A-Za-z ,.'!?\-]{7,}")
INTERESTING = lambda s: bool(CJK.search(s)) or (LATIN_SENT.search(s) and s.count(" ") >= 1)
IDLIKE = re.compile(r"^[A-Za-z0-9_./:\-]+$")   # asset paths / row keys / ids


def iter_fstrings(data):
    """Yield decoded strings by scanning for UE FString layout: int32 len + payload.
    len>0 => UTF-8 (len bytes incl NUL); len<0 => UTF-16LE (|len| units incl NUL)."""
    i, n = 0, len(data)
    while i + 4 <= n:
        ln = struct.unpack_from("<i", data, i)[0]
        if 1 < ln <= 2000 and i + 4 + ln <= n:
            raw = data[i+4:i+4+ln]
            if raw and raw[-1] == 0:
                try:
                    s = raw[:-1].decode("utf-8")
                    if s.isprintable() or CJK.search(s):
                        yield s; i += 4 + ln; continue
                except UnicodeDecodeError:
                    pass
        elif -2000 <= ln < -1 and i + 4 + (-ln)*2 <= n:
            cnt = -ln
            raw = data[i+4:i+4+cnt*2]
            if raw[-2:] == b"\x00\x00":
                try:
                    s = raw[:-2].decode("utf-16-le")
                    yield s; i += 4 + cnt*2; continue
                except UnicodeDecodeError:
                    pass
        i += 1


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "_extract")
    files = glob.glob(os.path.join(root, "**", "*.uexp"), recursive=True)
    files += glob.glob(os.path.join(root, "**", "*.uasset"), recursive=True)
    if not files:
        print(f"No assets under {root}"); return

    per_folder = Counter()
    per_file = Counter()
    samples = defaultdict(list)
    enc_counter = Counter()
    total_interesting = 0

    for f in files:
        try:
            data = open(f, "rb").read()
        except Exception:
            continue
        folder = os.path.dirname(os.path.relpath(f, root))
        for s in iter_fstrings(data):
            s = s.strip()
            if len(s) < 2:
                continue
            if INTERESTING(s) and not IDLIKE.match(s):
                per_folder[folder] += 1
                per_file[os.path.relpath(f, root)] += 1
                total_interesting += 1
                enc_counter["jp" if CJK.search(s) else "latin"] += 1
                if len(samples[os.path.relpath(f, root)]) < 6:
                    samples[os.path.relpath(f, root)].append(s)

    print(f"Scanned {len(files)} files. Interesting strings: {total_interesting} "
          f"(jp={enc_counter['jp']}, latin={enc_counter['latin']})\n")
    print("=== Top folders by translatable-string count ===")
    for folder, c in per_folder.most_common(20):
        print(f"  {c:6d}  {folder}")
    print("\n=== Top files + samples ===")
    for f, c in per_file.most_common(12):
        print(f"\n  [{c}] {f}")
        for s in samples[f]:
            disp = s if len(s) <= 80 else s[:77] + "..."
            print(f"        | {disp}")


if __name__ == "__main__":
    main()
