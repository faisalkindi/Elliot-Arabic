# HANDOFF — Elliot Arabic Localization (for the translating agent / Gemini)

> **Follow `PROCESS.md`** — the authoritative 12-step pipeline
> (Context + Glossary + Style Guide + AI Translation + Human Review + In-game QA).
> Work in **batches** per the Step-12 plan; append every approved line to
> `translation_memory.csv` (Step 11). Do not translate until the owner gives the go-ahead.

You are doing a **localization** (cultural adaptation, natural Arabic), **not a literal
translation**, of *The Adventures of Elliot: The Millennium Tales*.

- **Source language: JAPANESE** (the game's original). Do NOT use English as the source.
- **Target: Modern Standard Arabic**, game-friendly, natural — not stiff/literal.
- All files are **UTF-8**. Workspace root:
  `C:\Users\faisa\Ai\Mods Dev\Elliot\localization_workspace\`
- Game install (read-only, reference only):
  `H:\Steam\steamapps\common\The Adventures of Elliot_The Millennium Tales\`

---

## 1. THE FILE TO TRANSLATE (primary input)

`01_extracted_strings.jsonl`  — **16,183 records**, one JSON object per line.
Schema per line:
```json
{"id":"EL_<hash>","ftext_key":"<hash>","source_lang":"ja",
 "original_text":"<JAPANESE TEXT — translate this>","category":"dialogue|ui|menu|...",
 "speaker":"PCM000|NPC####|null","speaker_role":"player|npc|null","speaker_gender":"m|f|null",
 "chapter":"M01..M06|null","scene":"M01_E01|null","line_order":0,
 "placeholders":["<cf>","{0}",...],"placeholder_notes":"...","confidence":"high|medium|low"}
```
- Translate **`original_text`** (Japanese) → Arabic.
- Keep **`id`** / **`ftext_key`** unchanged — they map the string back into the game.
- **Use `speaker_gender`** for Arabic gender agreement, **`speaker`** + `04`'s character-voice list for register, and **`scene`/`line_order`** to localize dialogue in context (see `dialogue_scenes.md`).

Alternative format (same data, simpler): `scripts\_tools\UEExtractor\Paks_locres_commas.csv`
— columns `key,source,Translation`. You may fill the empty `Translation` column instead.

### Recommended OUTPUT
Write a new file `10_arabic_translation.jsonl` (do NOT overwrite `01`), each line:
```json
{"id":"EL_<hash>","arabic":"<ARABIC>","notes":"<optional>"}
```
(or fill the `Translation` column in a copy of the CSV).

---

## 2. NON-NEGOTIABLE RULES

1. **Preserve every tag and placeholder byte-for-byte**, in the same count. Found in the source:
   - Rich text: `<cf>` , `</>`
   - Icons: `<img id="RI_ICON_WPN_SWORD"/>`, `RI_ICON_WPN_BOMB`, `..._BOW`, `..._SPEAR`, `..._CHAIN`, `..._HAMMER`, `..._BOOMERANG`, `RI_ICON_LIFE_FULL`, `RI_ICON_STAR`, `RI_ICON_MONEY`, `RI_ICON_BUFF_*`, etc.
   - Buttons: `<btn id="MenuDecide"/>`, `<btn id="Attack1"/>`, `<btn id="Jump"/>`, etc. (some have `longpress="true"` / `width`/`height` attributes — keep them).
   - Format args: `{0}`, `{1}`, `{2}`, `{3}` (and any `%s`/`%d`).
   - Line breaks: literal `\n` — keep the same number; they control text-box pacing.
2. Do **not** translate `id` / `ftext_key`.
3. Follow `06_arabic_style_guide.md` for tone, RTL, Arabic punctuation (؟ ، ؛), numbers, and forbidden patterns.
4. Use `05_glossary.csv` for consistent names/terms (see §4 — Arabic column is still empty; agree terms first, then apply consistently).
5. **Skip** anything listed in `03_non_translatable_candidates.csv` (dev/debug strings, code IDs, ~50 corrupted/“mojibake” entries). **Flag, don't translate,** `02_uncertain_strings.csv` until reviewed.

---

## 3. SUPPORTING / CONTEXT FILES (read these first)

| File | What it gives you |
|------|-------------------|
| `00_file_audit.md` | What the game is, engine (UE5.6), where text lives, how it was extracted |
| `04_game_context.md` | **PLOT SYNOPSIS + character voices** (read fully), world, cast, places, tone |
| `dialogue_scenes.md` | Main-story dialogue in **scene order** (M01–M06) with speaker/gender tags — localize dialogue scene-by-scene from this |
| `05_glossary.csv` | ~70 recurring source terms (names/places/weapons/stats/UI) + should-translate flags; Arabic column empty by design |
| `06_arabic_style_guide.md` | Arabic tone, address/gender, honorifics, punctuation, RTL, line length, forbidden patterns |
| `02_uncertain_strings.csv` | 4,479 strings to review before translating |
| `03_non_translatable_candidates.csv` | 101 strings to SKIP |
| `09_localization_plan.md` | Overall plan / numbers |

### Key facts about the game (from the source data)
- Protagonist **エリオット (Elliot)**; fairy partner **フェイ (Faie)**.
- Named cast incl. マオ (Mao), ミュー (Myu), ヒューリア (Hyuria), ヒューリック (Hyurik),
  カーター (Carter), リュドミラ (Lyudmila), カイフリード (Kaifried), ディオナ (Diona),
  ヒルデブラント (Hildebrandt), イカロス (Icarus), オリバー (Oliver), ファウスタ (Fausta)…
- Places: 鍛錬の間, 光の間, 試練の聖堂, 時の扉 (Door of Time), エルダーツリー (Elder Tree),
  グランドツリー (Grand Tree), ドラゴンピラー (Dragon Pillar), directional caves.
- **7 weapon types**: Sword, Spear, Bomb, Boomerang, Chain, Hammer, Bow.
- HD-2D action RPG spanning four ages: 始まり (Beginning), 魔法 (Magic), 再建 (Reconstruction), 加護 (Blessing).

---

## 4. CURRENT STATE / CAVEATS
- `00`, `01` (source), `02`, `03`, `04`, `05`, `06`, `09` are built.
- `04`/`05` are grounded in the source text but romanizations are **phonetic/unverified**
  vs. official English names — treat readings as hints, keep names consistent regardless.
- `01` has **no per-row source-file path** (only the `ftext_key`, which is the re-injection
  locator). See `09` → Traceability.
- ~50–100 source entries are **mojibake** (Japanese mis-encoded, e.g. `ûyÕR…{0}cm`); these
  are flagged in `03`. Skip them.
- `category` values in `01` are a rough first-pass heuristic (many `unknown`); treat as hints.

---

## 5. VALIDATE YOUR OUTPUT (QA)
After translating, run the placeholder/tag/RTL checker (Python 3.10+):
```
python scripts\40_qa_validate.py <your_translation.csv>
```
It checks: missing/changed placeholders & tags, broken `<...>`/`</>`, untranslated rows,
inconsistent duplicates, glossary use, UI length, ASCII-vs-Arabic punctuation, RTL marks.
Grammar of protected tokens is defined in `scripts\placeholder_spec.py`.
