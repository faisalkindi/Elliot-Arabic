# 06 — Arabic Style Guide
**Game:** The Adventures of Elliot: The Millennium Tales · **Target:** Modern Standard Arabic (MSA), game-friendly

> This guide is language policy and does **not** depend on extracted strings, so it is
> usable now. Sections marked *(verify after extraction)* depend on in-game context
> (character genders, term usage) and will be tightened once `01_extracted_strings.jsonl`
> exists.

---

## 1. Overall tone
- **Natural, modern, immersive Arabic** — the way a well-localized JRPG reads (think quality fan/official RPG localization), not textbook or legalese.
- Fantasy adventure with time-travel; tone is **warm, adventurous, lightly heroic**, with room for humor (Faie the fairy companion). Avoid both street slang and stiff bureaucratic MSA.
- Prefer **فصحى ميسّرة**: full MSA grammar, but everyday, flowing vocabulary.

## 2. Formality level
- **Player-facing narration & dialogue:** standard MSA, neutral-warm.
- **UI/menus:** concise, imperative, consistent.
- Avoid heavy classical flourishes (e.g. avoid سَجْع / rhymed prose) unless a character is deliberately archaic.

## 3. Addressing the player / pronouns
- Default address to the player/Elliot: **masculine singular (أنتَ)** — Elliot is the male protagonist. *(verify after extraction that no string addresses a player-named/neutral avatar.)*
- For generic system prompts not tied to a character, prefer **neutral phrasing** that avoids gender where possible (e.g. الرجاء… / يُرجى…, مصدر verbal nouns) instead of forcing a gender.
- Keep a **single consistent register** of address; do not alternate أنتَ / أنتم for the same speaker target.

## 4. UI command style (imperatives — fixed list)
Use short verbal nouns or imperatives, kept consistent everywhere:

| English | Arabic (approved) | Notes |
|---------|-------------------|-------|
| Start / New Game | ابدأ / لعبة جديدة | |
| Continue | متابعة | verbal noun (cleaner on buttons than تابِع) |
| Back / Return | رجوع | |
| Confirm / OK | تأكيد / موافق | pick ONE per context and keep it |
| Cancel | إلغاء | |
| Yes / No | نعم / لا | |
| Save / Load | حفظ / تحميل | |
| Settings / Options | الإعدادات | |
| Quit / Exit | خروج | |
| Equip | تجهيز | |
| Use | استخدام | |
| Map | الخريطة | |
| Inventory / Items | الحقيبة / العناصر | decide one and lock in glossary |

> Rule: a UI verb chosen once is **frozen in `05_glossary.csv`** and reused identically.

## 5. Humor
- Localize **the joke, not the words.** Reproduce the *effect* in natural Arabic; never translate puns literally.
- Faie's banter should sound light and quick; keep sentences short. Mark any untranslatable wordplay in the row `notes` and propose an Arabic-native equivalent.

## 6. Honorifics / titles
- Render meaning, not Japanese honorifics. Use Arabic equivalents only where natural (سيّد/سيّدة، يا صاحبي، يا فتى). Do **not** invent honorifics where English/Japanese had none.

## 7. Names (people, places, factions)
- **Transliterate** proper names by default; keep them **consistent** (one spelling per name, locked in glossary).
  - Elliot → **إليوت** · Faie → **فاي** *(verify pronunciation against any in-game furigana/VO)*.
- Use a **light, readable transliteration**: avoid heavy diacritics on names; no hamza/madda overload.
- Place/faction names: transliterate unless the name is clearly **descriptive/meaningful**, in which case translate (decide per term in glossary, `should_translate`).
- **Magicite** (core item/system) → treat as a coined term; recommend **ماجيسايت** (transliterate) OR a translated **حجر السحر / شظايا السحر** — flag in glossary as a decision point. *(verify after extraction how the term is used mechanically.)*

## 8. Fantasy / sci-fi / mechanics terms
- Combat/RPG stats: prefer **familiar gaming Arabic** that players recognize:
  - HP → نقاط الصحة · MP → نقاط السحر · ATK → الهجوم · DEF → الدفاع · SPD → السرعة · EXP → الخبرة · Level → المستوى · Skill → مهارة · Ability → قدرة.
- Keep one term per concept across the whole game (enforced by glossary + QA `glossary_mismatch`).
- Coined/lore words: transliterate consistently; add a short gloss on first appearance only if the game itself does.

## 9. Punctuation rules (Arabic orthography)
- Use **Arabic punctuation**: `،` (comma), `؛` (semicolon), `؟` (question mark). Keep `.` `!` as-is.
- **No space before** punctuation; **one space after**. No double spaces.
- Quotation: use «…» or "…" consistently (recommend «…» for dialogue emphasis).
- Ellipsis: `…` (single char) — preserve count if the source uses it for pacing.
- Do **not** convert punctuation that is *inside a placeholder/tag*.

## 10. Numbers
- Use **Western Arabic numerals (0-9)** for all gameplay numbers (damage, prices, levels) — matches the UI font and avoids layout/towidth issues. *(verify the shipped font supports Eastern ٠-٩ before considering them; default to 0-9.)*
- **Never** localize digits that are inside placeholders (`%d`, `{0}`) — they are replaced at runtime.
- Keep units/currency order natural in Arabic (e.g. «100 قطعة ذهب»).

## 11. Line length / layout
- UI/menu labels: keep **short** — target ≤ ~28 characters (QA flags longer). Prefer verbal nouns to fit buttons.
- Dialogue: respect the source's **line breaks** (`\n`) exactly — they map to text-box pacing. Do not add or remove line breaks.
- Arabic is often **more compact** than English; use the saved space rather than padding.

## 12. RTL considerations
- Text is RTL but **embedded LTR tokens** (`%s`, `{0}`, `<tag>`, numbers, latin names) must keep their internal order — rely on the Unicode bidi algorithm; **do not** hand-insert LRM/RLM unless a real bug requires it (QA flags stray bidi controls).
- Verify mixed-direction strings render correctly **in-engine** (e.g. «لقد سددت %d ضررًا») — the `%d` must sit logically, not visually reversed.
- Brackets/parentheses: in RTL, `(` and `)` auto-mirror; write them in logical order (open before close in reading order).

## 13. Forbidden patterns
- ❌ Literal word-for-word renderings that break Arabic syntax (e.g. calquing English word order).
- ❌ Altering, translating, reordering, or spacing-out any placeholder/tag/escape (`{playerName}`, `%s`, `\n`, `<color>`…).
- ❌ Mixing dialects; no Gulf/Egyptian colloquialisms in MSA dialogue (unless a character is explicitly coded that way — none known *yet*).
- ❌ Inconsistent term/name spellings (same concept, two Arabic words).
- ❌ Over-formal filler (إنّ الأمر يتطلّب منك أن… where simply يجب أن… works).
- ❌ ASCII `?` `,` `;` inside Arabic text (use `؟` `،` `؛`).
- ❌ Translating debug/identifier/path strings (see `03_non_translatable_candidates.csv`).

## 14. Decision log (open term decisions — resolve in glossary)
| Term | Options | Recommended | Status |
|------|---------|-------------|--------|
| Magicite | ماجيسايت / حجر السحر / شظايا السحر | TBD | needs in-game context |
| Faie | فاي / فيّ | فاي | verify VO |
| Confirm vs OK | تأكيد / موافق | context-dependent | lock per screen |
| Inventory | الحقيبة / العناصر / المخزون | الحقيبة | provisional |

> Every decision here must be mirrored as a single row in `05_glossary.csv` once confirmed.
