# Pipeline notes (for contributors)

Working files, not needed to play. Everything player-facing is in the README and the Releases page.

## Layout

| Path | What |
|---|---|
| `PROJECT_STATE.md` | Running log: recon, every stage, the build that actually shipped (§8/§8A) |
| `00_file_audit.md` | Recon: UE 5.6 IoStore, unencrypted archive, no `.locres` folders — text is Japanese FText in DataTables |
| `01_extracted_strings.jsonl` | 16,183 source rows with speaker/gender/scene fields |
| `04_game_context.md` | Plot synopsis + character voices (built from `dialogue_scenes.md`) |
| `05_glossary.csv` | ~105 approved terms |
| `06_arabic_style_guide.md` | MSA style policy |
| `07_pilot_translation.csv` | Pilot that locked the register |
| `10_arabic_translation.jsonl` | Working translation output (id, ftext_key, arabic, notes) |
| `ar_final2.csv` | **THE SHIPPED TEXT** — UnrealLocres CSV, 16,910 entries, post-gender-pass |
| `dialogue_scenes.md` | Main-story dialogue, scene-ordered (M01–M06) |
| `translation_memory.csv` | Approved lines |
| `scripts/` | Extraction, QA validator (`40_qa_validate.py`), batch tooling |
| `installer/` | .NET 8 WinForms installer source (Arabic RTL UI) |

## Stages

1. Recon: UE 5.6 confirmed via jmap; usmap dumped at runtime. Text extracted with UEExtractor (CUE4Parse) → 16,183 Japanese strings.
2. Translate: Japanese → MSA, scene-ordered batches so addressee gender resolves from flow; glossary + style guide enforced; mechanical QA (`40_qa_validate.py`) then an independent adversarial review pass per batch, then a dedicated gender pass.
3. Build locres: `ar_final2.csv` → `Game.locres` via UnrealLocres.
4. Delivery (what shipped — see PROJECT_STATE §8.1): the installer rebuilds the game's encrypted base pak **locally** with repak (path-hash seed `1743788200`, Oodle), overlaying 6 files: `ar` + `it` copies of `Game.locres` (Arabic hijacks the Italian slot to become selectable), 4 Arabic `.ufont` faces (`.ufont` = 4-byte length prefix + raw TTF), and `DefaultEngine.ini` with `Slate.DefaultTextFlowDirection=2`.
5. RTL widget mod: a separate IoStore triple `zzz_Elliot_RTLfix_P.{pak,ucas,utoc}` (built with retoc) containing 14 widgets set to `Justification=InvariantRight` plus the Arabic title-logo texture (BC7).
6. Installer: .NET 8 self-contained single-file; Steam AppID 3483510 detection; embeds `payload.zip` (inject files + repak + Oodle dll + widget triple); backs up the original pak as `Elliot-Windows.pak.arabic_backup`; uninstall restores it.

## Rebuilding

Needs the game installed (Steam AppID 3483510), Python 3, and the toolbox (`repak`, `retoc`, `UnrealLocres`, `UEExtractor`, `jmap`, `WidgetEdit`) — not committed; see PROJECT_STATE §8B. Game files, extracted assets and built binaries are not committed.

- Locres: rebuild from `ar_final2.csv` with `UnrealLocres.exe`.
- Payload: regenerate `installer/payload.zip` from the inject tree + tools, then
  `cd installer && dotnet publish -c Release -r win-x64 --self-contained -p:PublishSingleFile=true -o publish`.
- If the game patches: re-derive `DefaultEngine.ini` from the new stock ini (only added line is `Slate.DefaultTextFlowDirection=2`) and re-check the pak seed.
