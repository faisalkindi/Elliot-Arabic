# PROJECT STATE — Elliot Arabic Localization (restore point)
> Read this FIRST after any context compaction to restore full project context.
> **Last updated 2026-07-25** — §8/§8A/§8B/§9 rewritten to document the build that actually SHIPPED
> (the file previously stopped at 2026-06-19, before the build phase, and described a plan
> that was later abandoned). Translation sections (§1–§7, §10–§11) are unchanged history.
>
> **STATUS: PROJECT SHIPPED.** Translation 100%, build done, installer released.

## 0. The project
- **Game:** The Adventures of Elliot: The Millennium Tales (冒険家エリオットの千年物語). Square Enix **Team Asano** + Claytechworks. **UE 5.6**, IoStore, HD-2D action RPG. Released 2026-06-18. Steam App **3483510**.
- **Install:** `H:\Steam\steamapps\common\The Adventures of Elliot_The Millennium Tales\` (project module `Elliot`; internal script module name **`LightStaff`**). ⚠️ **This path no longer exists as of 2026-07-25** — the game was moved or uninstalled. Re-locate it before any re-build.
- **Workspace:** `C:\Users\faisal\Ai\Mods Dev\Elliot\localization_workspace\` (note: older docs in this folder write the profile as `faisa` — that path does **not** exist; the real profile is **`faisal`**).
- **Goal:** **Arabic (MSA)** localization, translated **FROM JAPANESE** (decided — to preserve the original writers' nuance; English used only as a later comparison/QA reference).
- **Mode:** Gemini does the bulk translation; **I (Claude) am the QA gate AND will take over translation when Gemini's token quota runs out.**

## 1. Engine / extraction facts (verified)
- **UE 5.6 confirmed** (jmap `EngineVersion(5.6)`; bundled ONNX Runtime 1.20). Archive **unencrypted** (Oodle-compressed IoStore: `Elliot-Windows.pak/.ucas/.utoc` + `global.*`).
- **No `.locres`, no `GameText/Localize/<culture>` folders** (differs from Octopath 0). All text is **Japanese FText in DataTables** under `/Game/Data/DataTable/` (EventDataTable, ITEM, Common, Menu, etc.).
- **usmap:** `scripts/_tools/Mappings.usmap` (v4, dumped by jmap; UE5.6). Needed for FModel/UAssetGUI, NOT for .locres.
- **16,183 unique strings** extracted.

## 2. Tools (in `scripts/_tools/`, SHA-verified where noted)
- **jmap** (trumank/jmap v0.1.1) — usmap dump via `--pid` (needs ELEVATED admin; sandbox can't elevate → user runs it). `scripts/11_generate_usmap.ps1`.
- **retoc** (trumank/retoc v0.1.5) — IoStore convert; `oo2core_9_win64.dll` lives in `_tools/retoc/`.
- **UEExtractor** (SolicenTEAM v1.0.8.3, .NET 10, CUE4Parse) — **THE working extractor.** Crashes when stdout is redirected (CursorVisible bug) → run via PowerShell `Start-Process` (own console).
- UAssetGUI v1.1.0 — FAILED to parse cooked DataTables (RawExport); not used.
- ElliotLocExtract (custom C# CUE4Parse 1.2.2) — couldn't mount UE5.6 container (nuget too old); not used.
- `_reference/OCTOPATH TRAVELER 0_arabic.exe_extracted/` — extracted (via pyinstxtractor) Octopath 0 Arabic mod = Step 9 blueprint.

### Re-extract command (if ever needed)
1. Copy `_tools/Mappings.usmap` → `<PaksDir>\Mappings.usmap` (temp).
2. `Start-Process UEExtractor.exe -ArgumentList '"<PaksDir>"','-v=UE5_6','--auto-exit' -Wait` → writes `Paks_locres_commas.csv` (~16,189 lines) next to the exe. Delete the temp usmap after.
3. `python scripts/22_build_from_ueextractor.py` → rebuilds `01_extracted_strings.jsonl`.
4. `python scripts/93_enrich_context.py` → re-adds speaker/gender/scene fields.
5. `python scripts/96_flag_mojibake.py` and `98_fix_contaminated_sources.py` → clean 03 + 01.

## 3. Deliverables (in workspace)
| File | What |
|------|------|
| `00_file_audit.md` | engine/format audit |
| `01_extracted_strings.jsonl` | **16,183 source rows**, fields: id, ftext_key, source_lang, original_text, category, placeholders, confidence, **content_type, chapter, scene, block, line_order, speaker, speaker_role, speaker_gender** |
| `02_uncertain_strings.csv` | low-confidence/unknown |
| `03_non_translatable_candidates.csv` | **117** (junk/IDs + 16 mojibake) — SKIP these |
| `04_game_context.md` | **full PLOT SYNOPSIS + character voices** (built from `dialogue_scenes.md`) |
| `05_glossary.csv` | ~105 terms; `approved_arabic` being filled by Gemini (names transliterated, etc.) |
| `06_arabic_style_guide.md` | MSA style policy |
| `07_pilot_translation.csv` | pilot (~300) |
| `08_qa_*.md` | QA reports |
| `09_localization_plan.md` | plan + real numbers |
| `10_arabic_translation.jsonl` | **THE OUTPUT** — `{id, ftext_key, arabic, notes}`, currently **4,287 records** |
| `dialogue_scenes.md` | main-story dialogue scene-ordered (M01–M06, ~3,600 lines) |
| `translation_memory.csv` | approved lines |
| `HANDOFF.md` / `PROCESS.md` / `GEMINI_PROMPT.md` | Gemini's 12-step instructions |
| `REFERENCE_octopath0_method.md` | Step 9 build blueprint |
| `_retranslate_contaminated.txt` | 6 IDs (contaminated sources, mostly re-done) |
| `ar_final2.csv` | **THE SHIPPED TEXT** — UnrealLocres CSV (`key,source,target`; Arabic in `source`), 16,910 entries, post-gender-pass |
| `_fix/` | locres round-trip + fix passes; `ar_final3.locres`; `genreview/` = gender-only review pass |
| `_build/` | **abandoned `_P.pak` attempt** + `orig_locres/` (every shipped culture dumped as `.locres`/`.csv` — useful reference) |
| `installer/` | the C# installer, `payload2/` (what gets injected), `publish/Elliot Arabic Installer.exe` |
| `../_logo_work/`, `../_logo_export/` | Arabic title logo + `SST_clean.ttf` (the shipped font) |
| `../nexus_description_ar.txt` | Nexus release page text (Arabic) |

## 4. Scripts (`scripts/`)
- `placeholder_spec.py` — non-translatable token grammar (`<cf>`,`</>`,`<img.../>`,`<btn.../>`,`{0}`,`{Num:1}`,`%s`,`\n`).
- `40_qa_validate.py` — **QA validator.** Checks placeholders/tags, newlines, untranslated, **inconsistent dupes, glossary, UI length, ASCII punctuation, MSA-dialect, BiDi safety**. JA→AR-aware (skips identical/no-arabic when source isn't Japanese; relaxed length ratio; `""→"` quote normalization).
- `22_build_from_ueextractor.py` — build 01 from CSV (parse/dedup/categorize). 
- `93_enrich_context.py` — decode keys → speaker/gender/scene/order; writes `dialogue_scenes.md`.
- `95_review_batch.py` — coverage check + builds `_qa_batch_join.csv` (joins 10→01 by id).
- `96_flag_mojibake.py` — append mojibake to 03. `98_fix_contaminated_sources.py` — truncate contaminated 01 sources.
- `97_normalize_translation.py` — **STANDING newline-escape normalizer** (fixes Gemini's `\\n`→`\n` + real newlines→token). Run after EVERY batch before QA.
- `50_make_review_set.py` — builds `_review_set.md/.jsonl` (JA+AR+speaker/gender) for the independent reviewer subagent.
- Others: 90_scan_strings, 91_analyze_japanese, 92_key_context, 94_check_font, 20/21/30/31 parsers.

## 5. MY QA PIPELINE (run for every returned batch)
```
python scripts/97_normalize_translation.py                    # fix newline escaping (standing)
python scripts/95_review_batch.py <categories...>             # coverage + build _qa_batch_join.csv
python scripts/40_qa_validate.py _qa_batch_join.csv --out 08_qa_X.md
python scripts/50_make_review_set.py --n 45                   # then spawn a review subagent on _review_set.md
```
Independent-review layers (the "who checks me" solution): (1) mechanical QA above = model-agnostic; (2) **fresh reviewer subagent** back-translates + checks meaning/gender/register/MSA; (3) role-swap with Gemini on samples; (4) user.

## 6. PROGRESS — ✅ 100% COMPLETE (2026-06-19)
- **16,051 / 16,051 translatable rows translated (100.00%)**. 0 missing. (132 non-translatable correctly excluded in `03`: 117 mojibake + 15 `EL_Debug*` dev strings.)
- **ALL categories done:** ui, menu, system_message, tutorial, item/skill/quest, **dialogue 11,769**, unknown 535.
- **ALL main story M01–M06** + **8,566 side/NPC dialogue** + **535 stragglers** — all translated & QA-clean.
- **FINAL QA: 0 CRITICAL, 0 real dialect, 0 missing placeholders/newlines.** Remaining ~224 validator flags are all inherent/accepted: 191 duplicate-source NPC-chatter repeats (same generic line by many NPCs — fine), 18 soft UI-length hints, 6 intentional product titles kept in EN (Octopath/Bravely Default/Triangle Strategy) + wordless gasp, 9 minor glossary near-variants.
- **Done BY ME (Claude), full pipeline per bucket:** translator subagents (per-scene/chunk) → parity → mechanical QA → term-drift reconciliation → gender fixes → fresh independent back-translation reviewer → glossary update. Reviewers: M03 39/45, M04 41/44, M05 33/42, M06 70/78, **side 76/80 — all clean, no ship-blockers**.
- **Key systemic fixes:** Hilk=FEMALE, Mao=FEMALE (data flags unreliable), Eugène=MALE, 封魔=ختم الشرّ, phoenix=العنقاء(fem), file-wide term standardization (北の白楼, ميو tribe, Magin, Little Hope, etc.).
- Backups at each stage: `.pre_m03/m04/m05/m06/side/unknown.bak`.
- ~~NEXT = Step 9 BUILD~~ — **DONE.** See §8 for the method that shipped. English-comparison pass also DONE (§6b).
- **Post-translation fix passes (after this section was written):**
  - 2026-06-19 07:56–08:15 — locres round-trip fixes in `_fix/`: newline escaping (`fix_newlines.py`), untranslated-key sweep (`untranslated_keys.json`, `worklist.jsonl` → `batch_*.jsonl`/`out_*.jsonl`), quote normalization (`quotefix.csv`) → `ar_final2.locres`.
  - 2026-06-19 20:23 — `quit_fix.csv` + re-export → `ar_final3.locres`.
  - 2026-06-23 13:54–14:18 — **dedicated gender-only review pass** over the whole file: `_fix/genreview/` (`RUBRIC.md` = reviewer prompt, `build_batches.py` → `apply_fixes.py` → `finalize_apply.py`). Result: `ar_final2.csv` (+ `.pre_genderfix.bak`) → the shipped locres.
- **M03 + M04 done BY ME (Claude)** — per-chapter: translator subagents (per-scene, full-context for addressee gender) → merge+parity → mechanical QA → fresh back-translation reviewer → fixes → glossary update. M03 reviewer 39/45 clean; M04 reviewer 41/44 clean. **M04 notable fixes:** term drift (蛮族→البرابرة, Fozaval→معهد فوزاوال للأبحاث, kagari flower=篝→زهرة الموقد), addressee gender (E02→Fausta fem), and **Hilk (NPC0210) is FEMALE** (data + 女性) — corrected from masculine across E08/E09/E15. **ミュー族=قبيلة ميو standardized file-wide** (was عرق ميو in 16 old rows). Backups: `.pre_m03.bak`, `.pre_m04.bak`. Scene I/O in `_work/m03|m04/`.

## 6b. ENGLISH CROSS-CHECK — DONE (2026-06-19)
- **The English text WAS in the game** — inside the **AES-encrypted `Elliot-Windows.pak`** (the IoStore `.utoc` half is unencrypted JA; the `.pak` half holds `Content/Localization/Game/<culture>/Game.locres` for en/ja/fr/de/es/it/ko).
- **AES key:** `0x12992712E775A48B2CF002BE46619B1648C36F7212A91AB960825E0C023C62B5` (saved in `scripts/config.json`). Dumped via **AESDumpster 1.2.5** (`scripts/_tools/AESDumpster.exe`) on `Elliot-Win64-Shipping.exe`.
- **Extractor built:** `scripts/_tools/EnExtract/` — a CUE4Parse (built from source, `_cue4src/`) console app that mounts the pak with the key and dumps any culture's locres. English → `_extract/en_loc/en_text.json` (71,270 entries).
- **Joined EN↔JA↔AR:** `_extract/en_loc/joined_ja_en_ar.jsonl` — 95.4% of our rows matched to English (15,308; the 743 unmatched are 32-hex UI keys).
- **Full accuracy pass:** all 15,308 EN-matched rows compared (52 chunks). **95 genuine issues found (0.6%)**, all FIXED: 16 content-mismatches (re-translated from JA, EN-verified), 7 term/referent, 72 gender (EN pronouns revealed he/she the JA hid). Findings in `_extract/en_loc/EN_VERIFY_REPORT.md`. Backups `.pre_enverify.bak`.
- **Genders CONFIRMED by official EN:** Hirk=she, Māo=she, Euygene=he (all our calls were right). **Decision: names kept Japanese-faithful** (NOT aligned to official EN romanizations like Hichard/Hirk/Thiew — user choice). Official EN names recorded in `VERIFY_AGAINST_ENGLISH.md` for reference.

## 7. KEY DECISIONS & RULES
- **Source = Japanese** (English now also extracted & used for a full verification pass — see §6b).
- **`VERIFY_AGAINST_ENGLISH.md` (uncertain-decisions log):** every gender call (male↔female), inferred addressee, and coined name/transliteration we are NOT 100% sure of is logged there for a later cross-check against the official EN. **Append new uncertain calls each chapter.** Section A (gender/identity) is highest priority. Notable so far: **Hilk=FEMALE** (was masc), Fausta/Faie addressee gender, ~22 coined character names, kagari flower=meaning(زهرة الموقد).
- **REGISTER-SPLIT RULE (critical):** ANY row with `speaker_gender` → treat as **dialogue** (character register + gender per `04` voices + `dialogue_scenes.md`), regardless of its category label. ~11k dialogue lines are gendered.
- **ADDRESSEE-GENDER RULE (critical, found by independent review):** Arabic gender depends on grammatical person:
  - **1st person** (speaker about themselves — adjectives/predicates): use **`speaker_gender`**.
  - **2nd person** ("you" — verbs/pronouns like أنتَ/أنتِ, يمكنكَ/يمكنكِ): use the **ADDRESSEE's** gender, NOT the speaker's. **Default = MASCULINE** because Elliot (the male protagonist) is the usual listener; use feminine ONLY when the addressee is clearly female (e.g., someone addressing Hyuria/Faie/Reika/Mao).
  - **3rd person**: the referenced person's gender.
- **Dedup-by-source:** OK for ui/menu/system/items/skills/quests; **NOT for dialogue** (same line + different gender/context needs different Arabic).
- **Newline escaping:** Gemini writes `\\n`; `97_normalize` fixes it (single `\n` token is correct).
- **Batching:** structured categories proven clean → can combine; **dialogue checkpointed by chapter** (M01 passed). Always assert chunk-sum == unique count (don't drop strings).
- **Output format:** append to `10_arabic_translation.jsonl` = `{id, ftext_key, arabic, notes}`; never change id/ftext_key; reasoning/notes go in `notes`, never `arabic`.
- **Best LLM JA→AR:** close among Gemini 3.x Pro / Claude Opus 4.x / GPT-5.x; Claude strongest for tone+terminology → I'll translate well when I take over.

## 8. STEP 9 — BUILD/RE-INJECTION — ✅ DONE & SHIPPED (2026-06-19 → 2026-06-23)

### 8.0 What was ABANDONED (do not resurrect)
- The **Octopath 0 blueprint** (single legacy `ZZZ..._P.pak` override hijacking `GameText/Localize/EN-US` DataTables) does **not** apply: Elliot has no `Localize/<culture>` DataTables. Its per-language text is **`.locres`** in the encrypted pak (§6b). The dead attempt is still on disk: `_build/ZZZ_Elliot_Arabic_999_P.pak` and `_build/ZZZ_Elliot_Arabic_999_P_seedmatch.pak` (16 MB each) + `_build/ar_locres_map.json`. **Unused.**
- **"Arabic as a NEW selectable language"** was NOT achieved. The shipped mod **overwrites the Italian slot** (fallback plan). In-game: Settings → Language → pick «العربية», which appears **where «Italiano» was**.
- **Madika Arabic TRIAL** font was NOT shipped. Final font = **SST Arabic** (`_logo_work/SST_clean.ttf`, 250,152 bytes).

### 8.1 The method that SHIPPED — rebuild the base pak on the user's machine
The installer does all of this locally (nothing pre-built is redistributed except our own files):
1. `repak --aes-key <AES key from §6b> unpack Elliot-Windows.pak --output tree`
2. Overlay `payload2/inject/` onto `tree/` — 6 files:
   - `Elliot/Content/Localization/Game/**ar**/Game.locres`
   - `Elliot/Content/Localization/Game/**it**/Game.locres` ← **byte-identical to the `ar` one** (md5 `9a6890eb4e5e26aa2afac59c791ff139`, 2,378,948 bytes). Hijacking `it` is what makes Arabic selectable; the `ar` copy is there in case the culture resolves natively.
   - 4 × Arabic `.ufont` replacing the game's Latin faces in `Elliot/Content/Resources/UI/Font/Faces/`: `Gallery-Bold_LS`, `GarrickBold_LS`, `GarrickBoldItalic_LS`, `RapidBold_LS`.
   - `Elliot/Config/DefaultEngine.ini`
3. `repak pack --version V11 --mount-point ../../../ --compression Oodle -p 1743788200 tree Elliot-Windows.pak`
   - **`-p 1743788200` (= `0x67F018A8`) is the path-hash seed. It MUST match the original or the game won't mount the pak.**
   - Oodle compression needs `oo2core_9_win64.dll` next to `repak.exe` (both shipped in the payload).
4. Copy the separate IoStore widget mod into `Content\Paks\`: `zzz_Elliot_RTLfix_P.pak` / `.ucas` / `.utoc` (~9 MB) — see §8.3.
5. Original `Elliot-Windows.pak` is backed up in place as `Elliot-Windows.pak.arabic_backup`; uninstall restores it and deletes the 3 widget files.

### 8.2 The three things that make Arabic actually render RTL
1. **Font** — `.ufont` is NOT a UE asset: it is a **4-byte little-endian length prefix + the raw TTF bytes**. Verified: `RapidBold_LS.ufont` starts `28 d1 03 00` (= 250,152) then the TTF `00 01 00 00` header, and the remainder is byte-identical to `SST_clean.ttf`. All 4 faces are the same file. So swapping a font = prefix the TTF with its length.
2. **Engine-wide RTL flow** — `payload2/inject/Elliot/Config/DefaultEngine.ini` line 424, section `[ConsoleVariables]`:
   `Slate.DefaultTextFlowDirection=2`
   `ETextFlowDirection` (Slate/`TextLayout.h`) = **0 Auto · 1 LeftToRight · 2 RightToLeft · 3 Culture** (verified against Epic's UE 5.7 API docs). So `2` = **force RightToLeft**. This is the only mod-relevant line in that 564-line ini — the rest is the game's stock config, so the file must be re-derived from the shipped ini if the game ever patches it.
3. **Right-alignment of the widgets** — the cvar flows text RTL but does not re-align blocks; that's §8.3.

### 8.3 The RTL widget mod (`zzz_Elliot_RTLfix_P.*`)
- A **real IoStore mod** (`.pak`+`.ucas`+`.utoc` triplet, built with **retoc**), not a legacy pak — it lives alongside the rebuilt base pak and is loaded by name order (`zzz_`).
- Contents: **14 rebuilt text widgets** — `WBP_Com_Dialog`, `WBP_SpeechBubbleText`, `WBP_FacialSpeechBubbleText`, `WBP_CaptionText`, `WBP_TextList`, `WBP_COM_MenuList`, `WBP_Memo_ListItem`, `WBP_Memo_Parchment`, `WBP_Menu_MainStory_Window`, `WBP_Menu_SystemSetting_Tutorial`, `WBP_Menu_SystemSetting_Tutorial_Item`, `WBP_Tutorial_Active`, `WBP_Tutorial_Dialog`, `WBP_Tutorial_Pager` (JSON sources kept in `_extract/widgets/`) — **plus the Arabic title-screen logo texture**.
- Edit rule (`_fix/edit_widget.py`): for every export that has a `Text` TextProperty, set `Justification = InvariantRight`; **add** the property if absent, flip it if `Left`, and **leave `Center` / already-`Right` alone**. Round-tripped via `_tools/WidgetEdit/` (UAssetAPI console app).
- Arabic logo pipeline: `_logo_work/arabic_logo_820x424.png` → BC7 DDS (`arabic_logo_820x424.dds` / `logo_bc7.bin`) → packed as `t_tit_logo` (exports in `_logo_export/`; UE4-DDS-Tools credited in the Nexus description).

### 8.4 Final text numbers (as shipped)
- `ar_final2.csv` (UnrealLocres CSV, columns `key,source,target`; the **Arabic sits in `source`**, `target` is empty): **16,910 entries**, **16,340 Arabic (96.6%)**, 570 intentionally non-Arabic (numbers, latin product titles, symbols). Keys are `Namespace/Key`, e.g. `BonusItemName/DLC_TITLE_4_NAME`.
- Locres built/exported with `_tools/UnrealLocres.exe`. Lineage: `ar_Game.locres` → `ar_fixed` → `ar_final` → `ar_final2` → `ar_final3` → gender pass → shipped `payload2/.../Game.locres`.

## 8A. DISTRIBUTION — the installer (shipped)
- **Source:** `installer/Program.cs` (~700 lines, C# WinForms, .NET 8 `net8.0-windows`, `win-x64`, self-contained). Custom borderless gold-on-dark UI, **fully Arabic RTL** (`RightToLeft = Yes`, `RightToLeftLayout = true`), embedded `ui/ui_font.ttf` + `ui/ui_logo.png` as manifest resources. Footer credit: **«تعريب وإعداد: Kindiboy»**.
- **Game detection:** `HKCU\Software\Valve\Steam\SteamPath` → else `HKLM\SOFTWARE\WOW6432Node\Valve\Steam\InstallPath`, then parses every `"path"` in `steamapps\libraryfolders.vdf`, then reads `installdir` from `appmanifest_3483510.acf`; validates `Elliot\Content\Paks`. Manual folder picker as fallback (auto-appends the game subfolder name if the user picks the parent).
- **Payload:** `installer/payload.zip` embedded as the manifest resource `payload.zip` — the zipped `payload2/` tree = `inject/` (6 files) + `tools/repak.exe` + `tools/oo2core_9_win64.dll` + `widgets/` (3 files).
- **Installed marker** = presence of `zzz_Elliot_RTLfix_P.utoc`. Refuses to run if the game holds a lock on the pak ("اللعبة قيد التشغيل"), tells the user to run as admin on `UnauthorizedAccessException`.
- **Requirements told to the user:** game closed, **~8 GB free temp space**, admin if installed under Program Files, **no UE4SS or anything else needed**.
- **Artifacts:** `installer/publish/Elliot Arabic Installer.exe` (72.8 MB) + `.zip` (67.2 MB), built **2026-06-23 20:37**. `.pre_genfix.bak` copies = the pre-gender-pass build.
- **Nexus page text (Arabic):** `Elliot/nexus_description_ar.txt`. Credits repak, retoc, CUE4Parse/FModel, UnrealLocres, UE4-DDS-Tools.
- **Steam Deck:** `Elliot/_deck_deploy.py` — paramiko/SFTP push of the rebuilt pak + RTL widget mod (+ the VeryEasyPrices mod) to `deck@192.168.100.43`, size-verifies the upload, backs the original up to `Elliot-Windows.pak.vanilla_backup`.

## 8B. TOOLING FACTS worth keeping
- `_tools/`: `jmap` (usmap, needs elevation), `retoc` (IoStore ↔ legacy), `repak` (encrypted legacy pak unpack/pack), `UEExtractor` (the working JA text extractor), `UnrealLocres.exe` (locres ↔ CSV), `AESDumpster.exe` (the AES key), `FModel`, `EnExtract/` (custom CUE4Parse app that mounts the encrypted pak and dumps any culture's locres), `WidgetEdit/` (UAssetAPI widget JSON round-trip), `_cue4src/` (CUE4Parse built from source).
- **Side mods live in the same game folder but are NOT localization** (`Elliot/ue4ss_mods/`, `Elliot/_nexus_*`): UE4SS on this Square Enix UE5.6.1 build needs `UE4SS_Signatures/StaticConstructObject.lua` (custom AOB) + `EngineVersionOverride 5.6`, otherwise it fatal-errors "PS scan timed out". Released mods: InstantTransition, HalfRevive, SilentFaye, VeryEasyPrices.
- `Mods Dev` is **not a git repository** — none of this is version-controlled. Backups are `.bak` files only.

## 9. WORKFLOW STATE — ✅ CLOSED (project shipped 2026-06-23)
> Nothing is in flight. The per-batch pipeline below is **history**, kept because it is the
> recipe to reuse if the game patches and strings change. Re-open only for: a game update
> that invalidates the pak (re-run §8.1), or a reported translation bug (fix `ar_final2.csv`
> → rebuild locres → rebuild payload → rebuild installer).
>
> **Blocker if resumed:** the game is no longer at the `H:\Steam\...` path in §0 — re-locate
> it and update `scripts/config.json` (`game_paks`) first.

### 9-history. As of 2026-06-19 ~02:05
- **HANDOFF WAS LIVE: I (Claude) took over translation.** Gemini delivered M02 + the review fixes (verified landed), then was out of tokens for M03 → I translated **M03 myself** (see §6) end-to-end with the independence pipeline (translator subagents → mechanical QA → fresh reviewer subagent).
- **My per-batch pipeline (repeat for M04, M05, M06, side dialogue, unknown):**
  1. `python scripts/<extract>` → per-scene input files in `_work/<chap>/` (sorted by line_order), exclude already-done + 03 candidates.
  2. Spawn translator subagents (general-purpose) — **one batch = complete scenes in order** so addressee gender is resolved from flow. Brief them with `_work/<chap>/TRANSLATOR_BRIEF.md` (copy from m03), `04_game_context.md`, `05_glossary.csv`.
  3. Merge → parity check (count, no missing/extra/dupes) → append to `10` → `97_normalize` → `95_review_batch` (coverage) → `40_qa_validate`.
  4. Fix CRITICAL/HIGH (missing `\n`, term drift, gender) → re-validate to baseline.
  5. **Independent gate:** build review sample → spawn FRESH reviewer subagent (back-translation, adversarial) → apply its fixes → re-validate.
  6. Add new coined terms to `05_glossary.csv`.
- ~~**Next:** M04 dialogue next (same pipeline). Step 9 build remains parked.~~ — all chapters + side content finished; build done (§8).
- **Standing user preference:** end reviews with a ready-to-paste Gemini prompt **when Gemini is doing the work**; during my-handoff batches there's no Gemini prompt (I'm the translator) — just report results.

## 11. INDEPENDENT REVIEW — first audit result (2026-06-19)
Fresh reviewer subagent audited a 45-line sample of completed translations (back-translation + meaning/gender/register/MSA). Verdict: **40/45 clean — quality genuinely good** (consistent MSA, no dialect, tone fits speakers, all tags/punctuation preserved). Issues found (FIX LIST):
- **SERIOUS — gender:** `EL_NPC0180_P190_M020_NPC0180_f` uses **يمكنكِ** (fem. "you") but addressee is Elliot (male) → should be **يمكنكَ**. (This is what triggered the ADDRESSEE-GENDER RULE in §7.)
- Minor: `EL_002A77DE46F91466246AE1B58111B62D` "زيادة ضرر الحرجة" → **"زيادة الضرر الحرج"** (grammar).
- Minor: `EL_M01_E04_2000_M150_NPC0010_f` adds **مطيعين** (not in source; しっかり≠obedient) → drop it.
- Minor: `EL_M01_E07_2100_M050_NPC4229_m` 君に縁 ("connection to you") drifted to بيننا → should bond with **you**.
- Minor: `EL_M05_A3SWD_E01_2000_Title` 族 rendered **عرق** (race) → use **قبيلة/شعب ميو**.
These 5 fixes are pending (apply to `10_arabic_translation.jsonl`). The reviewer subagent process (`50_make_review_set.py` + a fresh Agent) is the standing semantic-QA layer for every future batch.

## 10. CLAUDE.md rules (carry forward)
- Check **Supermemory skill** first; use **EXA** (not WebSearch) + **REF** for docs; **never guess** — verify or say "I don't know".
