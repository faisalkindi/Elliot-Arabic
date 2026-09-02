#!/usr/bin/env python3
"""
94_check_font.py — inspect an OTF/TTF for Arabic localization suitability without
external deps. Checks: tables present, Unicode coverage of the Arabic block(s),
GSUB Arabic shaping ('arab' script + join features), and name/license strings.

Usage: python 94_check_font.py <font.otf>
"""
import sys, struct

path = sys.argv[1]
data = open(path, "rb").read()

def u16(o): return struct.unpack_from(">H", data, o)[0]
def u32(o): return struct.unpack_from(">I", data, o)[0]
def i16(o): return struct.unpack_from(">h", data, o)[0]

# --- sfnt table directory ---
num_tables = u16(4)
tables = {}
for i in range(num_tables):
    rec = 12 + i * 16
    tag = data[rec:rec+4].decode("latin1")
    off = u32(rec + 8); length = u32(rec + 12)
    tables[tag] = (off, length)
print("tables:", ", ".join(sorted(tables)))
for need in ("cmap", "GSUB", "GPOS", "name"):
    print(f"  {need}: {'present' if need in tables else 'MISSING'}")

# --- cmap coverage ---
codepoints = set()
if "cmap" in tables:
    coff = tables["cmap"][0]
    ntab = u16(coff + 2)
    best = None
    for i in range(ntab):
        rec = coff + 4 + i * 8
        plat = u16(rec); enc = u16(rec + 2); suboff = coff + u32(rec + 4)
        fmt = u16(suboff)
        # prefer a Unicode subtable (plat 3 enc 1/10, or plat 0)
        if (plat, enc) in ((3, 1), (3, 10), (0, 3), (0, 4), (0, 6)) or best is None:
            best = (suboff, fmt)
            if (plat, enc) in ((3, 10), (0, 6)):
                break
    suboff, fmt = best
    if fmt == 4:
        segX2 = u16(suboff + 6); segc = segX2 // 2
        endo = suboff + 14
        starto = endo + segX2 + 2
        for s in range(segc):
            end = u16(endo + s*2); start = u16(starto + s*2)
            for cp in range(start, min(end, 0xFFFF) + 1):
                codepoints.add(cp)
    elif fmt == 12:
        ngroups = u32(suboff + 12)
        for g in range(ngroups):
            go = suboff + 16 + g * 12
            sc = u32(go); ec = u32(go + 4)
            for cp in range(sc, ec + 1):
                codepoints.add(cp)

def covered(lo, hi):
    rng = [cp for cp in range(lo, hi + 1)]
    have = sum(1 for cp in rng if cp in codepoints)
    return have, len(rng)

blocks = {
    "Arabic (0600-06FF)": (0x0600, 0x06FF),
    "Arabic Supplement (0750-077F)": (0x0750, 0x077F),
    "Arabic Presentation Forms-A (FB50-FDFF)": (0xFB50, 0xFDFF),
    "Arabic Presentation Forms-B (FE70-FEFF)": (0xFE70, 0xFEFF),
    "ASCII (0020-007E)": (0x20, 0x7E),
}
print("\ncoverage:")
for name, (lo, hi) in blocks.items():
    h, t = covered(lo, hi)
    print(f"  {name}: {h}/{t}")
# key Arabic letters present?
sample = {0x0627: "ا", 0x0628: "ب", 0x062C: "ج", 0x0644: "ل", 0x0645: "م", 0x0647: "ه", 0x064A: "ي", 0x0621: "ء"}
miss = [c for c in sample if c not in codepoints]
print("  core Arabic letters missing:", [hex(c) for c in miss] or "none")

# --- GSUB: Arabic script + shaping features ---
def list_scripts_features(tag):
    if tag not in tables:
        return None, None
    base = tables[tag][0]
    script_list = base + u16(base + 4)
    feat_list = base + u16(base + 6)
    scripts = []
    ns = u16(script_list)
    for i in range(ns):
        rec = script_list + 2 + i * 6
        scripts.append(data[rec:rec+4].decode("latin1"))
    feats = []
    nf = u16(feat_list)
    for i in range(nf):
        rec = feat_list + 2 + i * 6
        feats.append(data[rec:rec+4].decode("latin1"))
    return scripts, feats

gs, gf = list_scripts_features("GSUB")
if gs is not None:
    print("\nGSUB scripts:", sorted(set(gs)))
    print("  has 'arab' script:", "arab" in gs)
    join = {"init", "medi", "fina", "isol", "rlig", "liga", "calt", "ccmp", "mark", "mkmk"}
    print("  shaping features present:", sorted(set(gf) & join))
else:
    print("\nGSUB: MISSING -> Arabic letters will NOT join/shape correctly")

# --- name / license ---
if "name" in tables:
    no = tables["name"][0]
    count = u16(no + 2); stroff = no + u16(no + 4)
    wanted = {0: "copyright", 1: "family", 2: "subfamily", 13: "license", 14: "license_url"}
    print("\nname/license:")
    for i in range(count):
        rec = no + 6 + i * 12
        pid = u16(rec); eid = u16(rec + 2); nid = u16(rec + 6)
        ln = u16(rec + 8); off = u16(rec + 10)
        if nid in wanted:
            raw = data[stroff + off: stroff + off + ln]
            try:
                s = raw.decode("utf-16-be") if (pid == 3 or pid == 0) else raw.decode("latin1")
            except Exception:
                s = raw.decode("latin1", "replace")
            s = s.strip()
            if s:
                print(f"  [{wanted[nid]}] {s[:200]}")
