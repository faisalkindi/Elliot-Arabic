# 00 — File Audit

**Game:** The Adventures of Elliot: The Millennium Tales
**Game files:** `H:\Steam\steamapps\common\The Adventures of Elliot_The Millennium Tales`
**Target language:** Arabic (Modern Standard Arabic, game-friendly)
**Audit date:** 2026-06-18
**Auditor:** localization engineering agent (read-only inspection; no game files modified)

---

## 1. Engine / framework identification

| Property | Finding | How verified |
|----------|---------|--------------|
| Engine | **Unreal Engine 5** | `.utoc`/`.ucas` IoStore containers + `Elliot-Win64-Shipping.exe` layout |
| Packaging | **IoStore / Zen** (`.pak` + `.ucas` + `.utoc` triplet) | Files in `Elliot\Content\Paks` |
| IoStore TOC version | **8 = `ReplaceIoChunkHashWithIoHash`** → engine **≥ 5.3** | Read `.utoc` header bytes directly (magic `-==--==--==--==-`, version byte `0x08`) |
| Likely minor version | **5.4 or newer** (exact minor unconfirmed) | `Engine\Plugins\NNE\NNERuntimeORT` (consolidated NNE plugin shipped in UE 5.4; Experimental in 5.3) + `DirectML.dll` (ORT-DML backend). **Indicator, not proof.** |
| Project (game) module | **`Elliot`** | Folder `Elliot\`, exe `Elliot-Win64-Shipping.exe` |
| Encryption (AES) | **Unknown — to be confirmed** | Not determinable from headers alone; FModel will report on first load. Series history is mixed (Octopath 1/2 unencrypted; Triangle Strategy & Octopath 0 encrypted). |

> Exact engine minor version and encryption status are the two **open unknowns**. Both resolve the moment a `.usmap` dump / FModel load is attempted (see §5).

## 2. Relevant folders

| Folder | Relevance |
|--------|-----------|
| `Elliot\Content\Paks\` | **ALL game content** (assets, text, data tables) — locked inside IoStore archives |
| `Elliot\Binaries\Win64\` | Shipping exe; target dir for UE4SS / mappings dumper / ASI loader |
| `Engine\` | Stock UE engine content (fonts, slate, renderer) — not game text |

## 3. File-type inventory (complete; non-binary files only)

| File | Size | Translatable? |
|------|------|---------------|
| `Elliot\Content\Paks\Elliot-Windows.pak` | ~3.5 GB | Container (holds cooked assets) |
| `Elliot\Content\Paks\Elliot-Windows.ucas` | **~13.5 GB** | **Container — holds essentially all text** |
| `Elliot\Content\Paks\Elliot-Windows.utoc` | ~28 MB | Table of contents for the above |
| `Elliot\Content\Paks\global.ucas` / `.utoc` | ~3 MB | Engine global container (script objects) |
| `Engine\Config\StagedBuild_Elliot.ini` | 0 bytes | No (empty) |
| `Engine\Content\...\*.ttf / *.cur / *.bin / *.tps` | small | No (stock engine fonts/cursor/renderer) |

**There are NO loose text files** (no `.json`, `.csv`, `.xml`, `.po`, `.locres`, `.txt`, dialogue files, or localization tables) anywhere on disk. Everything player-facing is **cooked inside `Elliot-Windows.ucas`.**

## 4. Likely text sources (inside the IoStore archive, once extracted)

Based on the Team Asano HD-2D lineage (Octopath Traveler I/II, Triangle Strategy, DQ3 HD-2D Remake — all same studio/engine family), expect:

| Source type | Expected asset(s) | Category mapping |
|-------------|-------------------|------------------|
| Localization string tables | `*.locres` (per-culture, e.g. `en/Game.locres`) | dialogue, UI, system_message |
| Master text DataTable | `GameTextEN`-style `.uasset`/`.uexp` | dialogue, UI, lore |
| Item data | `ItemDB`-style DataTable | item_name, item_description |
| Skill/ability data | `AbilityData` / `AbilitySetData` / `SupportAbilityData` | skill_name, skill_description |
| Enemy data | `EnemyDB` | item/lore (names) |
| Character/job data | `PlayableCharacterDB` / `JobData` | UI, lore |
| Shops | `ShopList` / `PurchaseItemTable` | UI, item_name |
| Global params | `GameParamDefineTable` / `BattleParamDefineTable` | mostly non-text (numeric) |
| Quest/world | `WorldMapTable`, quest tables | quest_title, quest_description |
| Dialogue scripts | possibly Lua (`.lub` in `LuaScriptBin/`) — **Triangle Strategy did this** | dialogue, tutorial |

> Exact asset names/paths for **Elliot** are **not yet known** and must be discovered by browsing the extracted archive in FModel. The table above is the lineage-based expectation, not a confirmed manifest.

## 5. Files needing special extraction tools

**Everything.** Nothing is readable with a plain text editor. Required pipeline (UE5 IoStore):

1. **`Mappings.usmap`** — mandatory. UE5 cooks *unversioned properties*; no parser can read any asset without the mappings file. Generated at **runtime** via UE4SS (Dumpers → "Generate .usmap") or by injecting UnrealMappingsDumper / `jmap` into the running game.
2. **retoc** (`to-legacy`) — convert Zen → legacy `.uasset/.uexp` for editing/parsing. (ZenTools = backup.)
3. **FModel** — browse/inspect, export `.locres` to JSON/CSV, locate the real asset paths.
4. **UAssetGUI** — read/export DataTables to JSON (needs the `.usmap` + exact engine version).
5. (Repack later, for the localized build) **retoc** (`to-zen`).

See `scripts/README.md` for the concrete command chain.

## 6. Risks & unknowns

| # | Risk / unknown | Impact | Mitigation |
|---|----------------|--------|------------|
| R1 | **`.usmap` not yet available** — hard blocker for ALL extraction | Cannot extract a single string until resolved | Generate via UE4SS/dumper (needs one game launch with injected DLL) — **awaiting user approval** |
| R2 | Exact UE minor version unknown | retoc/UAssetGUI need correct `--version` | UE4SS log prints it on first launch; try `UE5_4` first |
| R3 | Possible AES encryption | Extraction needs the key | FModel reports on load; key extractable via AESKeyFinder if present |
| R4 | Text may be split across `.locres` **and** DataTables **and** Lua | Partial extraction risk; must cover all three | Audit all asset types after first extraction |
| R5 | Arabic is **not** a shipped culture | No `ar/` locres to mirror; new culture may need engine/font support | Engineering concern for the *build* phase, not extraction |
| R6 | Game just released (2026-06-18) | No community `.usmap` / tooling presets exist yet | We generate our own |
| R7 | 13.5 GB archive | Full extraction is slow/large | Use retoc `--filter` to target only text/data folders |

## 7. Audit conclusion

- Engine and structure are **fully identified**: UE5 IoStore, project module `Elliot`, all text cooked into `Elliot-Windows.ucas`.
- **Step 2 (extraction) is currently BLOCKED** on producing a `Mappings.usmap`, which requires a one-time runtime dump (game launch + injected dumper/UE4SS).
- No fabricated strings will be produced. Downstream files (`01`–`09`) are scaffolded with correct schemas and marked `PENDING EXTRACTION` until the blocker is cleared.
- Language-policy deliverables that do **not** depend on extracted text (`06_arabic_style_guide.md`) are drafted now.
