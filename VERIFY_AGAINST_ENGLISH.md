# VERIFY AGAINST OFFICIAL ENGLISH — uncertain decisions log

**Purpose:** Every decision below was made from the **Japanese source + scene context only** (no access to the official English yet). When we later pull the game's English translation, cross‑check each item to confirm. Items are ranked by impact: **gender/identity errors change Arabic grammar everywhere a character appears**, so verify Section A first.

Status legend: ⚠️ = inferred, could be wrong · 🔶 = transliteration (spelling/identity to confirm) · 🟡 = meaning‑vs‑translit judgment call.

---

## A. GENDER & IDENTITY decisions  ⚠️ (verify FIRST — affects all of a character's lines)

| Character / row(s) | JA evidence | What we decided | Why uncertain → check in EN |
|---|---|---|---|
| **Hilk (ヒルク / NPC0210)** — M04 E08, E09 (all NPC0210 lines), E15_3000_M340/M360, E08_M110/M170 | data `speaker_gender=f`; E15_3000_M340 JA says 「ヒルクという**女性**」 ("a woman named Hilk") | **FEMALE.** Translators first made her a male elder; I corrected to feminine throughout: `السيدة هيلك`, `مشغولة`, `ترى`, `تخبره… أنها سمعت`, Elliot's `هل أنتِ السيدة هيلك؟` | Confirm Hilk is female in EN (she/her). If EN uses he/him, revert all NPC0210 lines to masculine. **HIGH PRIORITY.** |
| **Fausta (ファウスタ / NPC0150)** addressee — `EL_M04_E02_1000_M070_PCM000_m` | Scene flow: Fausta greets Elliot (M060), Marnie sent him to her | Elliot addresses **Fausta (female)** → `بأنكِ هنا` | Confirm the person Elliot says "Marnie told me **you** were here" to is Fausta, not Icarus (male). If Icarus → `بأنك`. |
| **Faie (フェイ) addressee** — `EL_M02_E07_1000_M220/M230_PCM000_m` | M240 Faie: "I remembered, I was asked to save the kingdom" | The recalled plea addresses **Faie (female)** → `أنتِ الأمل الأخير` / `أنقذيها` | Confirm in EN the "you are the last hope" line in M02_E07 is directed at Faie (vs Elliot in M01, which is masculine). |
| **Elliot as addressee** — `EL_NPC0180_P190_M020_NPC0180_f` | addressee is Elliot (male protagonist) | fixed `يمكنكِ` → `يمكنكَ` | Standing ADDRESSEE‑GENDER rule. Confirm fine. |
| **Hyuria addressee** — `EL_M03_E15_2000_M260_PCM000_m` (`انتظري`) | Elliot addresses Hyuria (NPC0010, f) through M240–M260 | feminine `انتظري` | Confirm Elliot is addressing Hyuria here (not a male). |
| **General ADDRESSEE‑GENDER rule** | — | 2nd‑person "you" follows the **listener's** gender (default masculine = Elliot); feminine only for clearly female addressees | Spot‑check a few EN lines to confirm who is being addressed in ambiguous scenes (esp. group scenes). |

---

## B. COINED CHARACTER NAMES — transliterations  🔶 (confirm official EN spelling AND gender)

These were transliterated phonetically from katakana; the official EN may use a different romanization (or reveal gender). Verify spelling for each:

| JA | Our Arabic | Likely EN (guess) |
|---|---|---|
| マオ | ماو | Mao |
| ミュー | ميو | Myu / **Mew?** |
| ヒューリア | هيوريا | Hyuria |
| ヒューリック | هيوريك | Hyurik |
| カーター | كارتر | Carter |
| リュドミラ | ليودميلا | Lyudmila |
| カイフリード | كايفرايد | Kaifried |
| ディオナ | ديونا | Diona |
| **ヒルク** | هيلك | Hilk — **also confirm FEMALE (see A)** |
| イカロス | إيكاروس | Icarus |
| ヒルデブラント | هيلدبراند | Hildebrandt |
| ユイジーヌ | يوجين | Eugène? |
| ファウスタ | فاوستا | Fausta |
| レイカ | رايكا | Reika |
| マーニー | مارني | Marnie |
| オリバー | أوليفر | Oliver |
| ヒカルド | هيكاردو | Hicardo / Ricardo? |
| イチル | إيتشيرو | Ichiru |
| クレイドル | كرايدل | Cradle |
| ラーウェイ | راوي | Rāwei (revealed = Elliot's mother) |
| ロウエル | رولل | Lowell? |
| マギー | ماغي | Maggie? |
| **ゴギョウ** | غوغيو | Gogyou (M04) |

> Note: `エリオット→إليوت (Elliot)`, `フェイ→فاي (Faie)` are already confirmed via OFFICIAL EN in glossary.

---

## C. COINED PLACE / FACTION / ITEM / TERM names  🔶

| JA | Our Arabic | Notes / what to confirm |
|---|---|---|
| ウルヴ族 | قبيلة أولف | "Ulv/Wolf tribe" — confirm EN name + spelling |
| ミュー族 | قبيلة ميو | "Mew tribe" — confirm EN |
| フロギー族 | قبيلة فروغِي | "Froggy tribe?" |
| ウェイゼン | ويزن | city/faction + department store name |
| フォマニット研究所 | معهد فومانيت للأبحاث | "Fomanit Research Institute" |
| フォザワール | فوزاوال (معهد فوزاوال للأبحاث) | "Fozaval/Fozawar Institute" — had 3 spellings, unified |
| エルダーゲート | بوابة إيلدر | "Elder Gate" (= باب الزمن / Gate of Time) |
| エルダーツリー | شجرة إيلدر | "Elder Tree" |
| マギカニ | ماغيكاني | "Magicani" creature |
| 月鏡の盾 | درع مرآة القمر | "Moon‑Mirror Shield" (meaning‑based) |
| ブーストコア | نواة الدفع | "Boost Core" |
| ツール | تول | currency unit — confirm EN name |
| バケネコ | القط المسحور | "Bakeneko / Monster Cat" |
| 憎悪の魔獣 | الوحش السحري المكروه | enemy type |

---

## D. MEANING vs TRANSLITERATION judgment calls  🟡

Where we chose to **translate the meaning** instead of transliterating (or vice‑versa) — confirm the EN treats it the same way:

| JA | Our Arabic | Our call | Verify |
|---|---|---|---|
| かがりの花 | زهرة الموقد | **meaning** (篝 = bonfire/brazier), matched item name — NOT transliterated "Kagari" | If EN treats "Kagari" as a proper flower name, switch to transliteration |
| 蛮族 | البرابرة | generic "barbarians/savages" (the Ulv are 蛮族) | confirm EN uses a generic word, not a proper faction name |
| ライトスタッフ | لايت ستاف | transliterated (in‑world artifact "Light Staff") | confirm it's an artifact name, not UI |
| 魔石 | حجر السحر | translated "magic stone" | confirm EN naming (Magicite? Magic Stone?) |
| クリティカルダメージ上昇 | زيادة الضرر الحرج | "Critical Damage Increase" | confirm EN combat term |
| Age names (始まり/再建/加護/魔法) | البداية / إعادة الإعمار / البركة / السحر | translated as era names | confirm the four "Age of …" names in EN |

---

## M05 additions (chapter done by Claude, 2026-06-19)

**Gender/identity ⚠️:**
- **NPC0130** — unnamed female scholar (data `f`); her JA register is masculine‑leaning/casual‑scholarly but we followed the `f` flag. Confirm gender + whether she has a name in EN.
- Kept addressee‑gender per rule (Elliot=masc; Hyuria/Lyudmila/Faie=fem). Lyudmila (NPC0080) addressed feminine.

**Coined names/transliterations 🔶:**
- バイカン → بايكان (Baikan, merchant)
- カロテシア → كاروتيشيا (Carotesia, place)
- カイ → كاي (Kai, NPC0200 village/faction leader — **distinct from Kaifried/كايفرايد**; confirm it's a separate character)
- 北の白楼 → البرج الأبيض الشمالي (Northern White Tower)
- 三賢者 → الحكماء الثلاثة (Three Sages)
- 白銀の鈴 → الجرس الفضي (Silver Bell)

**Meaning‑vs‑translit / naming judgment 🟡:**
- **火の鳥 / 不死鳥 → العنقاء** (phoenix) — UNIFIED three variants (طائر النار / الفينيق / العنقاء) onto العنقاء; 不死鳥山 → جبل العنقاء. **Confirm EN: are "Firebird" and "Phoenix Mountain" the same entity or distinct names?**
- 萌芽の時代 → عصر البزوغ ("Age of Budding") — confirm EN era name.
- 神獣 → الوحش الإلهي (divine beast); 氷結の呪い/封印 → لعنة/ختم التجميد (standardized التجميد).
- 封魔の奥義 → سرّ ختم السحر ("secret art of sealing magic").

---

## M06 additions (finale, done by Claude, 2026-06-19)

**Gender/identity ⚠️ (HIGH priority):**
- **ラーウェイ / Rāwei (راوي) infant gender** — Carter believes the baby is his **son** (息子), but Rāwei is revealed to be Elliot's **mother** (female). Translators rendered feminine when comforting "don't cry Rāwei" but masculine where Carter says "my son." **Confirm EN: what gender/pronoun for baby Rāwei at the M06_E06/E08 birth scenes vs the adult reveal.**
- **NPC0060 dual identity (E24)** — same NPC ID reads as **Rāwei** (mother) in the battle/family thread and **Mao** in the orphanage-epilogue thread. Confirm which character per thread in EN.
- **火の鳥/Cradle = العنقاء is grammatically FEMININE** — standardized feminine agreement (نائمة, استيقظت, كانت). Confirm Cradle is she/her in EN.

**Coined names 🔶:**
- ノイーワン → نويوان (Noiwan, leader of the Three Sages)
- ウザン → أوزان (Uzan, Ichiru's adoptive father, ex-guard-captain)
- 黒の賢者 → الحكيم الأسود (Black Sage); 白の賢者 → الحكيمة البيضاء (White Sage, NPC0530, female)
- グランドツリー → الشجرة العظيمة (Grand Tree); 琥珀のペンダント → القلادة الكهرمانية (amber pendant)

**Note:** A4 era code kept verbatim (`A4の時代`); 萌芽の時代 aligned to عصر النشوء.

---

## SIDE-CONTENT additions (8,566 side rows + 535 stragglers, done by Claude, 2026-06-19)

**Gender/identity ⚠️ (data errors found):**
- **Mao (マオ/ماو) data flag is UNRELIABLE in SP** hint rows** — several SP chunks rendered Mao masculine before correction. Mao is FEMALE everywhere. Fixed 5 rows; glossary now notes it. Confirm in EN.
- **Eugène (NPC0020) is MALE** despite a `f` data flag in some rows — handled correctly. Confirm.
- **Sandy (サンディ/NPC4379) is a FEMALE girl** — one masculine ref fixed. Confirm.
- A genuine **mistranslation** was caught and fixed (`EL_S04_N04_1000_M100_PCM000_m`: AR was unrelated to JA "I'll gather the fan cactus — can I leave Sandy with you?").

**Coined names/transliterations 🔶 (many — confirm EN spellings):**
- Characters: ساندي (Sandy), باكانتي (Bacante), نيك (Nick), ناكاتاني (Nakatani), تادوكورو (Tadokoro), ساهيكي (Saheki), هيرالدا (Hiralda), فرون (Furon), أوزان (Uzan), نويوان (Noiwan).
- Tribes: قبيلة إليفان (Elephan), قبيلة راتّي (Ratty), قبيلة ترين (Trin) — all "savage" clans alongside قبيلة أولف.
- Places: قرية الأمل الصغير (Little Hope), المنطقة البيضاء (White Area), المنطقة الغربية (West Area), نيفا ويذر (Neva Wither), درب إيدا (Edda Trail), سهل فرون (Furon Plains).
- Items/creatures: ماغين (Magin), حجر امتصاص السحر (magic-absorbing stone), إيليغ (Eleg), فطر باميل (Pamil mushroom), وندرفول (Wonderful toy), شيراكوتشي/بوكونا (plants).
- **NOTE:** カロテシア used as BOTH a place (glossary) and a female NPC name — confirm which in EN.
- Faie ability call-outs rendered inconsistently (meaning vs translit: الإشعال/تشاكّا etc.) across dialogue vs flavor — confirm against the EN skill names.

**Non-shippable:** 15 `EL_Debug*` dev strings excluded (added to `03_non_translatable_candidates.csv`). A few dev-note strings (EL_NPC2311, EL_M06_E13_6000 etc.) leaked into the dialogue set and were translated faithfully but ideally should not ship.

---

## E. HOW TO VERIFY (later, at the English‑comparison pass)
1. Extract the official **English** DataTable text the same way we extracted Japanese (English IS in the files — `source_lang` field / a second culture table).
2. Join EN by `ftext_key`/`id` to our rows.
3. For **Section A**: read the EN line for each character to confirm pronouns (he/she) and who is addressed → fix any Arabic gender that disagrees.
4. For **Sections B/C**: copy the EN proper‑noun spelling → update transliteration + `05_glossary.csv` → re‑run the term‑standardization pass over `10_arabic_translation.jsonl`.
5. For **Section D**: match the EN's translate‑vs‑transliterate choice.

> This log is appended to as new chapters are translated. New uncertain calls from M05+ go here too.
