# PROCESS — the 12-step localization pipeline (authoritative)

> ⚠️ **Status columns below are 2026-06-18 history — all 12 steps are now DONE.** The
> "Step 9 — in-game testing" section describes a *plan* that was **superseded**: the shipped
> build does NOT use a `_P.pak` override, does NOT use the Madika font, and does NOT add
> Arabic as a new culture (it hijacks the Italian slot). See **`PROJECT_STATE.md` §8** for
> what actually shipped. Keep this file for the per-batch translation recipe only.

Both the foundation agent (Claude) and the translating agent (Gemini) follow **this**
process. Formula: **Context + Glossary + Style Guide + AI Translation + Human Review + In-game QA.**
Source = **Japanese**. Target = **Arabic (MSA)**. Translation is gated on the owner's go-ahead.

| # | Step | Owner | Status | Where |
|---|------|-------|--------|-------|
| 1 | Collect all text | Claude | ✅ done | `01_extracted_strings.jsonl` (16,183) · method in `00_file_audit.md` |
| 2 | Classify by type | Claude | ✅ done | `category` field in `01` (dialogue 11,787 · ui 2,837 · item 351 · system 223 · menu 180 · skill 164 · quest 76 · tutorial 30 · unknown 535) |
| 3 | Game context file | Claude | ✅ done | `04_game_context.md` |
| 4 | Glossary | Claude (terms) → Gemini/human (Arabic) | ◑ terms done, Arabic empty | `05_glossary.csv` |
| 5 | Style guide | Claude | ✅ done | `06_arabic_style_guide.md` |
| 6 | Pilot sample (200–500) | Gemini → human review | ⏸ awaiting go-ahead | `07_pilot_translation.csv` |
| 7 | AI translation in a pipeline | Gemini | ⏸ | output → `10_arabic_translation.jsonl` |
| 8 | Linguistic/contextual review | human (+ Gemini) | ⏸ | annotate `10_…` / `08_qa_report.md` |
| 9 | In-game test | Claude (build tooling) + human | ⛔ needs re-injection build (see below) | — |
| 10 | Linguistic + technical QA | `40_qa_validate.py` + human | ◑ tool ready | `08_qa_report.md` |
| 11 | Translation memory | Gemini/human append | ✅ scaffold ready | `translation_memory.csv` |
| 12 | Work in batches | all | ✅ plan below | this file |

## Step 7 — exact inputs to give the model per batch
For every batch, the prompt MUST include:
1. **Context** — `04_game_context.md`
2. **Glossary** — `05_glossary.csv` (apply approved terms; propose new ones, don't freelance)
3. **Style guide** — `06_arabic_style_guide.md`
4. **The batch text** — rows from `01_extracted_strings.jsonl` (the `original_text`)
5. **Hard rule** — never alter/translate/reorder placeholders & tags:
   `<cf>`, `</>`, `<img id="…"/>`, `<btn id="…"/>`, `{0}`/`{1}`/`%s`/`%d`, `\n`.
   Keep `id`/`ftext_key` untouched. Output to `10_arabic_translation.jsonl`.

## Step 12 — batch plan (order chosen for leverage + consistency)
Run the cycle each batch: **translate → review → (in-game test when available) → update glossary/style → next.**

| Batch | Content | ~count | Why this order |
|-------|---------|--------|----------------|
| 0 — Pilot | 200–500 mixed (dialogue/ui/item/skill/quest/system) | ~300 | Lock tone + terminology before scale |
| 1 | UI + menu | ~3,000 | Short, high-visibility; sets UI verb conventions early |
| 2 | system_message + tutorial | ~250 | Fixed phrasings; feed glossary |
| 3 | item_name/description + skill_name/description | ~515 | Terminology-heavy; lock with glossary |
| 4 | quest_title/description | ~76 | — |
| 5 | dialogue | ~11,800 | Largest; split into sub-batches by scene/speaker, leaning on the TM |
| last | uncertain (`02`) review | 535 | Reclassify/skip case-by-case |

Skip everything in `03_non_translatable_candidates.csv`.

## Step 9 — in-game testing (separate technical phase, not yet built)
Putting Arabic back into the game and testing it requires a build pipeline Claude will set up later:
- **Re-injection:** map `ftext_key` → game data and repack (`retoc to-zen` → `.utoc/.ucas/.pak` in `Content/Paks/~mods`), OR via a localization (`.locres`) overlay.
- **Arabic font:** the game's shipped font lacks Arabic → must import/assign an Arabic UE font asset (or set up font fallback for the Arabic range).
  - **Chosen font (owner's decision): `C:\Users\faisa\Downloads\alfont_com_MadikaArabicTRIAL-Regular.otf`** (Madika Arabic) — verified good: all core Arabic glyphs + GSUB `arab` shaping (init/medi/fina/isol/rlig/calt/ccmp/liga) + ASCII. Use this for the build.
  - Note: it's a TRIAL license; owner has reviewed and accepted the licensing risk. (If a clean-license swap is ever wanted, drop-in OFL alternatives: Noto Sans Arabic, IBM Plex Sans Arabic, Cairo.)
- **Text shaping (verified):** UE5.6 supports Arabic via the text widget **Text Shaping Method = Full Shaping** (auto-selected for RTL text). Ensure the localized text widgets use Auto/FullShaping, not KerningOnly.
- **RTL layout:** UE applies RTL at the **text level, not layout** — text flows RTL but menus/HUD do **not** auto-mirror. Full UI mirroring is manual (parent text under HorizontalBox/VerticalBox; CanvasPanel/GridPanel won't mirror). Check text-box fit & button overflow.
- This is the riskiest unknown (Arabic is not a shipped culture). Schedule after the pilot is approved.

### PARKED build-phase tasks (decided 2026-06-18; do at Step 9, not now)
- **Re-injection method:** Octopath 0 Arabic mod = single legacy `_P.pak` override (no IoStore repack) — see `REFERENCE_octopath0_method.md`. BUT Elliot's text layout DIFFERS from Octopath 0 (no `GameText/Localize/<culture>` tables; probes for Localize/GameText/Culture/EN-US all = 0). Elliot's runtime language mechanism is **not yet cracked**.
- **Owner's goal:** add **Arabic as a NEW selectable language** (not overwrite English). Feasibility UNCONFIRMED — depends whether Elliot's language list is data-driven (pak-moddable) or hardcoded C++ (needs UE4SS, or not pak-feasible). Fallback = overwrite an existing language slot (Octopath 0 method, guaranteed).
- **Investigate at build phase:** how Elliot stores/loads per-language text (find the .locres/culture mechanism — note container directory index is compressed so earlier greps were unreliable; use FModel/UE4SS), the language-settings widget, and culture-switch logic. Then decide new-entry vs overwrite.

## Definition of done (per the owner's summary)
A line is "done" only after: AI draft → human linguistic review → in-game QA pass → saved to the translation memory.
