#!/usr/bin/env python3
"""
21_parse_datatable_json.py — pull strings out of UE DataTable / asset JSON exports.

Input: JSON produced by either
  - UAssetGUI:  `UAssetGUI tojson In.uasset Out.json UE5_4 Mappings`
  - FModel:     right-click asset -> Save Properties (.json)

Walks the JSON tree and collects every string-valued leaf, recording the full
dotted key-path (so a translator can see e.g. Rows.ITEM_0007.Description.SourceString).
Heuristically skips obvious non-text leaves (asset paths, enum names, GUIDs).

Run AFTER exporting DataTables to JSON. Output: ../_extract/_rows_datatable.jsonl

Usage:
  python 21_parse_datatable_json.py            # scans work_extract for *.json
  python 21_parse_datatable_json.py file.json
"""
import json, sys, os, glob, re

SKIP_KEYS = {"$type", "ObjectName", "ObjectPath", "ClassName", "Outer",
             "PackageGuid", "Guid", "Name", "Flags", "StructGUID"}
# leaf values that are clearly not player text:
PATH_LIKE = re.compile(r"^/(Game|Engine|Script)/|\.[A-Za-z0-9_]+$|^[A-F0-9]{16,}$|^None$|^ENone")
IDENT_LIKE = re.compile(r"^[A-Z][A-Za-z0-9_]*$")     # ItemId, EWeaponType, etc.
HAS_LETTER = re.compile(r"[A-Za-zÀ-ɏ]")
# UE FText export usually looks like {"CultureInvariantString": "..."} or
# {"SourceString": "...", "Namespace": "...", "Key": "..."}
FTEXT_VALUE_KEYS = ("SourceString", "CultureInvariantString", "LocalizedString", "String")


def looks_translatable(key, val):
    if not isinstance(val, str) or not val.strip():
        return False
    if key in SKIP_KEYS:
        return False
    if PATH_LIKE.search(val):
        return False
    if IDENT_LIKE.match(val) and " " not in val:
        return False
    if not HAS_LETTER.search(val):
        return False
    return True


def walk(node, path, rows, src_file, ftext_hint=None):
    if isinstance(node, dict):
        # Detect FText-shaped dict: capture its namespace/key for traceability
        ns = node.get("Namespace") or node.get("namespace")
        ky = node.get("Key") or node.get("key")
        for vk in FTEXT_VALUE_KEYS:
            if vk in node and isinstance(node[vk], str) and looks_translatable(vk, node[vk]):
                rows.append({
                    "source_file": src_file, "key_path": path + "." + vk,
                    "ue_namespace": ns, "ue_key": ky,
                    "original_text": node[vk],
                })
        for k, v in node.items():
            walk(v, f"{path}.{k}" if path else k, rows, src_file)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, f"{path}[{i}]", rows, src_file)
    elif isinstance(node, str):
        # bare string leaf
        leaf_key = path.rsplit(".", 1)[-1].split("[")[0]
        if leaf_key not in FTEXT_VALUE_KEYS and looks_translatable(leaf_key, node):
            rows.append({
                "source_file": src_file, "key_path": path,
                "ue_namespace": None, "ue_key": None,
                "original_text": node,
            })


def main():
    here = os.path.dirname(__file__)
    cfg = json.load(open(os.path.join(here, "config.json"), encoding="utf-8"))
    if len(sys.argv) > 1:
        targets = [sys.argv[1]]
    else:
        root = os.path.join(here, cfg["work_extract"])
        targets = glob.glob(os.path.join(root, "**", "*.json"), recursive=True)
        targets = [t for t in targets if not os.path.basename(t).startswith("_rows")]

    if not targets:
        print("No DataTable .json found. Export DataTables via UAssetGUI tojson / FModel first.")
        return

    out_path = os.path.join(here, cfg["work_extract"], "_rows_datatable.jsonl")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    total = 0
    with open(out_path, "w", encoding="utf-8") as out:
        for t in targets:
            try:
                data = json.load(open(t, encoding="utf-8"))
            except Exception as e:
                print(f"[WARN] {t}: {e}"); continue
            rows = []
            walk(data, "", rows, os.path.abspath(t))
            for r in rows:
                out.write(json.dumps(r, ensure_ascii=False) + "\n")
            total += len(rows)
            print(f"  {os.path.basename(t)}: {len(rows)} strings")
    print(f"Wrote {total} rows -> {out_path}")


if __name__ == "__main__":
    main()
