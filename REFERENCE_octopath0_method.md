# Reference: how the Octopath Traveler 0 Arabic mod was built
> Reverse‑engineered from `OCTOPATH TRAVELER 0_arabic.exe` (a PyInstaller GUI installer by "MohmmadFadel1987"). This is the closest sibling to Elliot (Square Enix HD‑2D, UE5 IoStore) → our **Step 9 blueprint**.

## The method (confirmed)
1. **Single override pak.** One legacy `.pak` placed in `…\Octopath_Traveler0\Content\Paks\`:
   `MohmmadFadel1987-ZZZZZZ_999999_9999999_P.pak` (62.9 MB).
   - The `ZZZZZZ_999999_9999999` name makes it sort **alphanumerically last** → it overrides everything; `_P` = patch suffix.
   - **A loose legacy `.pak` overrides the IoStore (.ucas/.utoc) base** in this UE5 engine family. **No `retoc to-zen` / IoStore repacking needed.** ← big simplification.
2. **They hijacked the ENGLISH locale's text tables.** Inside the pak: DataTables at
   `/Game/Local/DataBase/GameText/Localize/EN-US/SystemText/GameTextCharacter` (and siblings).
   - Structure is `m_id` → `m_gametext` rows; they replaced the **EN‑US** `m_gametext` values with **Arabic**.
   - Player selects **English** in‑game → sees **Arabic**. (No `.locres` in the pak — these games use per‑culture **DataTables**, exactly like Elliot.)
   - Pak contained **17 `.uasset` + 34 `.uexp`** (the GameText DataTables).
3. **Arabic font shipped as UE font assets.** Pak contained **25 `.ufont`** assets — the game's font replaced with **Bahij TheSansArabic** (an **SIL OFL**, freely‑licensable Arabic font). This is what makes Arabic glyphs render in‑engine.
4. **Distribution = a GUI installer** (PyInstaller + customtkinter) that:
   - Auto‑detects the game across `Steam\steamapps\common`, `SteamLibrary\…`, `Program Files\Epic Games`, `Program Files\WindowsApps`.
   - Copies the `_P.pak` into `…\Content\Paks\`.
   - (`myfont.ttf` in the bundle is only the **installer window's** Arabic UI font, not the game font.)

## What this means for ELLIOT (Step 9 plan)
- ✅ **Build one `_P.pak`** (legacy, via UnrealPak/repak) named to sort last (e.g. `ZZZ_Elliot_Arabic_999_P.pak`), drop in `Elliot\Content\Paks\`. No IoStore repack.
- ✅ **Inject Arabic into the EN‑US GameText DataTables** (the same `Localize/EN-US/…` structure Octopath 0 used) so selecting **English** shows Arabic. Map our `ftext_key` → the DataTable `m_id` rows.
- ✅ **Pack the Arabic font as `.ufont` assets** replacing the game's font (we'd use Madika; note Octopath 0 used the OFL **Bahij TheSansArabic** — a clean‑license alternative).
- ✅ Optional: a similar GUI installer for distribution.

## ⚠️ Important re‑opened question
Octopath 0 clearly has a **`GameText/Localize/EN-US/`** per‑culture DataTable structure. This strongly implies **Elliot has the same** — i.e. the **English text IS in the files** after all, in EN‑US DataTables that the source‑text extractor (which returns the Japanese source) didn't surface. This does **not** change our decision to localize **from Japanese**, but:
- It's where we **inject** the Arabic (overwrite EN‑US rows).
- English text is available as a **comparison reference** if ever wanted.
- **TODO (Step 9):** locate Elliot's `…/GameText/Localize/EN-US/…` DataTables and confirm the `ftext_key` ↔ `m_id` mapping.

## Extracted reference files (local, do not redistribute)
`C:\Users\faisa\Ai\Mods Dev\Elliot\_reference\OCTOPATH TRAVELER 0_arabic.exe_extracted\`
- `…\Content\Paks\MohmmadFadel1987-ZZZZZZ_999999_9999999_P.pak` — the real mod pak (study its structure)
- `installer.pyc` — install logic
