#!/usr/bin/env python3
"""
20_parse_locres.py — parse Unreal Engine *.locres string-table files into rows.

Implements the documented UE .locres binary format (versions Legacy/0 ..
Optimized_CityHash64_UTF16/3), the format used by UE4.25+ and UE5. Each row is
emitted to ../_extract/_rows_locres.jsonl with full traceability.

This is the most reliable text source for UE games (UI, dialogue, system text all
land here under namespaces). Run AFTER 10_extract_iostore.ps1 has produced the
.locres files under _extract.

Usage:
  python 20_parse_locres.py                 # scans config.work_extract for *.locres
  python 20_parse_locres.py path\to\file.locres

Output row schema (JSONL):
  { source_file, namespace, key, source_string_hash, original_text }
"""
import struct, sys, os, json, glob

LOCRES_MAGIC = bytes([0x0E,0x14,0x74,0x75,0x67,0x4A,0x03,0xFC,
                      0x4A,0x15,0x90,0x9D,0xC3,0x37,0x7F,0x1B])
# version enum
V_LEGACY, V_COMPACT, V_OPTIMIZED, V_OPTIMIZED_CH64 = 0, 1, 2, 3


class Reader:
    def __init__(self, data): self.d, self.p = data, 0
    def u32(self):
        v = struct.unpack_from("<I", self.d, self.p)[0]; self.p += 4; return v
    def i32(self):
        v = struct.unpack_from("<i", self.d, self.p)[0]; self.p += 4; return v
    def i64(self):
        v = struct.unpack_from("<q", self.d, self.p)[0]; self.p += 8; return v
    def fstring(self):
        n = self.i32()
        if n == 0:
            return ""
        if n > 0:  # UTF-8 (ASCII), includes null terminator
            raw = self.d[self.p:self.p + n]; self.p += n
            return raw.split(b"\x00", 1)[0].decode("utf-8", "replace")
        # negative => UTF-16LE, abs(n) code units incl null terminator
        n = -n
        raw = self.d[self.p:self.p + n * 2]; self.p += n * 2
        return raw.decode("utf-16-le", "replace").split("\x00", 1)[0]


def parse(path):
    with open(path, "rb") as f:
        data = f.read()
    r = Reader(data)
    version = V_LEGACY
    if data[:16] == LOCRES_MAGIC:
        r.p = 16
        version = data[16]; r.p = 17

    string_table = None
    if version >= V_OPTIMIZED:
        table_off = r.i64()
        save = r.p
        r.p = table_off
        count = r.i32()
        string_table = []
        for _ in range(count):
            s = r.fstring()
            if version >= V_OPTIMIZED_CH64:
                r.i32()  # ref count, ignored
            string_table.append(s)
        r.p = save

    rows = []
    ns_count = r.u32()
    for _ in range(ns_count):
        if version >= V_OPTIMIZED:
            r.u32()  # namespace hash
        namespace = r.fstring()
        key_count = r.u32()
        for _ in range(key_count):
            if version >= V_OPTIMIZED:
                r.u32()  # key hash
            key = r.fstring()
            src_hash = r.u32()
            if version >= V_OPTIMIZED:
                idx = r.i32()
                text = string_table[idx] if string_table and 0 <= idx < len(string_table) else ""
            else:
                text = r.fstring()
            rows.append({
                "source_file": os.path.abspath(path),
                "namespace": namespace,
                "key": key,
                "source_string_hash": src_hash,
                "original_text": text,
            })
    return rows


def main():
    here = os.path.dirname(__file__)
    cfg = json.load(open(os.path.join(here, "config.json"), encoding="utf-8"))
    if len(sys.argv) > 1:
        targets = [sys.argv[1]]
    else:
        root = os.path.join(here, cfg["work_extract"])
        targets = glob.glob(os.path.join(root, "**", "*.locres"), recursive=True)

    if not targets:
        print("No .locres files found. Run 10_extract_iostore.ps1 first "
              "(and confirm text actually lives in .locres vs DataTables).")
        return

    out_path = os.path.join(here, cfg["work_extract"], "_rows_locres.jsonl")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    total = 0
    with open(out_path, "w", encoding="utf-8") as out:
        for t in targets:
            try:
                rows = parse(t)
            except Exception as e:
                print(f"[WARN] failed to parse {t}: {e}")
                continue
            for row in rows:
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
            total += len(rows)
            print(f"  {os.path.basename(t)}: {len(rows)} entries")
    print(f"Wrote {total} rows -> {out_path}")


if __name__ == "__main__":
    main()
