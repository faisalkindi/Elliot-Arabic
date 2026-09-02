# 09 — Localization Plan

**Status:** Foundation complete (extraction + organization). **No translation performed.**
Source language: **Japanese**. Target: **Arabic (MSA)**. Updated with real extraction numbers.

## Numbers (actual)
| Metric | Value |
|--------|-------|
| Total unique strings extracted | **16,183** |
| High-confidence | 15,716 |
| Medium-confidence | 366 |
| Low-confidence | 101 |
| Uncertain → review (`02`) | 4,479 |
| Non-translatable / skip (`03`) | 101 (incl. ~50–100 mojibake + dev/debug/IDs) |
| Japanese strings | 15,589 |
| Non-Japanese (credits/dev/code) | 594 |
| Strings containing placeholders/tags | 8,899 |

### Category breakdown (first-pass heuristic — treat as hints)
dialogue 10,555 · unknown 4,502 · skill_description 329 · ui 248 · item_description 229 · system_message 175 · menu 145

## Main source
- All text lives in `Elliot-Windows.ucas` (UE5.6 IoStore, unencrypted, Oodle).
- Extracted via UEExtractor (CUE4Parse) using a runtime-dumped `Mappings.usmap` (UE5.6).
- Canonical input: `01_extracted_strings.jsonl`. Raw form: `scripts/_tools/UEExtractor/Paks_locres_commas.csv`.

## Traceability (honest status — relates to your Core Rule 3)
- Each string carries its **FText key** (`ftext_key`) — this is UE's stable identifier and is what re-injects the translation into the game. ✅
- **Per-asset source-file path is NOT available** from this extraction method (the source-text tool aggregates by key, not by originating DataTable/.locres). The `source_file`/`context` fields requested in the brief's Step-2 schema are therefore **not populated**. Mitigation if needed: re-derive key→asset mapping via FModel/CUE4Parse JSON export (extra step, deferred).

## Recommended translation workflow (when you approve translation)
1. Translate `original_text` (JA) → AR into a **new** file `10_arabic_translation.jsonl`, keyed by `id`/`ftext_key` (never overwrite `01`). See `HANDOFF.md`.
2. Follow `06_arabic_style_guide.md`; enforce `05_glossary.csv` for names/terms.
3. Skip `03`; review `02` first.
4. Preserve all tags/placeholders (`<cf>`,`</>`,`<img.../>`,`<btn.../>`,`{0}`,`\n`).
5. QA each batch with `scripts/40_qa_validate.py`.
6. (QA phase) Extract official **English** as a cross-reference to sanity-check nuance.

## Tools / scripts (in `scripts/`)
- Built & verified: `placeholder_spec.py`, `40_qa_validate.py`, `22_build_from_ueextractor.py`, `90_scan_strings.py`, `91_analyze_japanese.py`.
- Extraction pipeline: `11_generate_usmap.ps1` (jmap), UEExtractor (`_tools/`), `20/21/30/31` parsers.
- `_tools/`: jmap, retoc, UAssetGUI, UEExtractor, ElliotLocExtract (all SHA-verified where applicable).

## Biggest risks
- R1 — Per-string asset-path traceability missing (see above); key-based re-injection still works.
- R2 — ~50–100 mojibake source entries (flagged in `03`); a cleaner re-extract could recover them.
- R3 — Category labels are heuristic; many `unknown`. Human/agent pass needed for accurate categorization.
- R4 — Romanizations in `04`/`05` are phonetic and unverified vs. official EN names.
- R5 — Arabic is not a shipped culture; **build-phase** font/RTL/culture-registration work is separate from extraction.

## State of deliverables
| File | State |
|------|-------|
| `00_file_audit.md` | ✅ complete |
| `01_extracted_strings.jsonl` | ✅ 16,183 strings (UTF-8); ⚠ no per-row source_file/context |
| `02_uncertain_strings.csv` | ✅ 4,479 |
| `03_non_translatable_candidates.csv` | ✅ 101 |
| `04_game_context.md` | ✅ built from source data (labelled confidence) |
| `05_glossary.csv` | ✅ ~70 source terms; Arabic column intentionally empty |
| `06_arabic_style_guide.md` | ✅ complete (policy) |
| `07_pilot_translation.csv` | ⏸ empty — awaiting your go-ahead to translate |
| `08_qa_report.md` | ◑ validator ready; no report until something is translated |
| `09_localization_plan.md` | ✅ this file |
| `HANDOFF.md` | ✅ instructions for the translating agent |

## Next step before full translation
You decide whether to translate. Everything is staged for a translating agent (Gemini) per `HANDOFF.md`. Optional pre-translation polish: re-extract to recover mojibake (R2) and add key→asset traceability (R1).
