# Localization extraction & QA scripts

Pipeline for extracting translatable text from **The Adventures of Elliot: The Millennium Tales**
(Unreal Engine 5, IoStore) and validating Arabic translations.

> **Status:** The extraction scripts (`10`, `20`, `21`) are written against documented
> formats but have **not yet been run against Elliot's data**, because they require a
> `Mappings.usmap` that does not exist yet (see `../00_file_audit.md` §5, risk R1).
> The QA validator (`40`) is format-independent and runnable today against any CSV.

## Prerequisites (one-time setup)

| Tool | Purpose | Source |
|------|---------|--------|
| Python 3.10+ | run the `.py` parsers/validators | python.org |
| **retoc** | extract/convert IoStore Zen → legacy `.uasset` | github.com/trumank/retoc |
| **FModel** | browse archive, export `.locres` → JSON | github.com/4sval/FModel |
| **UAssetGUI** (CLI) | export DataTables → JSON (`tojson`) | github.com/atenfyr/UAssetGUI |
| **`Mappings.usmap`** | REQUIRED for any UE5 asset parse | generated at runtime — see below |
| UE4SS *or* UnrealMappingsDumper / jmap | produce the `.usmap` | docs.ue4ss.com / github.com/TheNaeem/UnrealMappingsDumper |

### Generating `Mappings.usmap` (the blocker)
1. Install UE4SS into `H:\...\Elliot\Binaries\Win64\` (or inject UnrealMappingsDumper).
2. Launch the game once; open the UE4SS console → **Dumpers** tab → *Generate .usmap*.
   (UE4SS also prints the exact **engine version** in its log — record it.)
3. Copy the produced `Mappings.usmap` into `scripts/_tools/Mappings.usmap`.

> This is the only step that runs the game with injected code. It is read-only w.r.t.
> game files but requires explicit user approval before it is performed.

## Configuration

Edit `config.json` (paths + engine version) before running anything:
```json
{
  "game_paks": "H:\\Steam\\steamapps\\common\\The Adventures of Elliot_The Millennium Tales\\Elliot\\Content\\Paks",
  "engine_version": "UE5_4",          // CONFIRM via UE4SS log; UE5_3 / UE5_4 / UE5_5 ...
  "aes_key": "",                       // fill only if FModel reports encryption
  "usmap": "_tools/Mappings.usmap",
  "retoc_exe": "_tools/retoc.exe",
  "work_extract": "../_extract",       // raw extracted assets (gitignored, large)
  "out_dir": ".."                      // where 01_*..09_* live
}
```

## Run order

```bash
# Step 2a — extract text-bearing assets from IoStore (Zen -> legacy uasset)
pwsh ./10_extract_iostore.ps1            # uses retoc to-legacy with --filter for text/data dirs

# Step 2b — parse UE .locres string tables -> rows
python ./20_parse_locres.py              # scans _extract for *.locres

# Step 2c — parse DataTable JSON (exported via UAssetGUI tojson / FModel) -> rows
python ./21_parse_datatable_json.py      # scans _extract for *.json DataTables

# Step 2d — merge + assign IDs + categorize -> 01_extracted_strings.jsonl
python ./30_build_extracted.py

# Step 3 — split uncertain / non-translatable -> 02_*, 03_*
python ./31_classify_filter.py

# Step 8 — QA a translated file (07_pilot_translation.csv) -> 08_qa_report.md
python ./40_qa_validate.py ../07_pilot_translation.csv
```

## What each script guarantees

- **Never** writes to the game directory. Reads `game_paks`, writes only under `out_dir`/`work_extract`.
- Preserves a full trace for every string: `source_file`, `key`/`row`, `path`.
- Treats placeholders/tags as opaque — see `placeholder_spec.py` for the token grammar
  that `40_qa_validate.py` enforces (printf `%s`/`%d`, ICU `{0}`/`{Name}`, UE rich-text
  `<...>`/`</>`, `\n`/`\r`, sprite `<img .../>`, `$name`). Tokens are never altered.
