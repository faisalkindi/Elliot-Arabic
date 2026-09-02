# 04 — Game Context

**Game:** The Adventures of Elliot: The Millennium Tales (冒険家エリオットの千年物語)
**Built from:** the 16,183 extracted Japanese source strings (`01_extracted_strings.jsonl`) + verified public/official facts (labelled).
**Confidence labels:** `[SRC]` = derived from the extracted game text · `[OFF]` = official/store/press (verified) · `[INF]` = inference (treat as tentative) · `[?]` = unknown.

> Source language is **Japanese**. Romanizations below are **phonetic reading aids** unless marked `[OFF]`; verify official English spellings later.

---

## Genre
- HD-2D **action RPG** with real-time, weapon-based combat and a controllable fairy partner. `[OFF]`
- Confirmed by source: stat/combat vocabulary — 攻撃力 (attack), 防御力 (defense), 素早 (agility), 体力 (HP), クリティカル (critical), チャージ (charge), レベル, スコア, 満腹度 (satiety). `[SRC]`

## Setting / world
- A journey across **four ages / a thousand-year span** (time-travel framing). The four ages appear in-text as: **始まり** (Beginning), **魔法** (Magic), **再建** (Reconstruction), **加護** (Blessing). `[SRC][OFF]`
- Time travel is mechanic + lore: **時の扉** "Door of Time" (×61), described in-text as **時を渡る魔法の扉** ("a magic door that crosses time"). `[SRC]`
- **Magic (魔法, ×638)** is central; **加護の魔法** ("blessing magic") is associated with a **祈りの間** (Hall of Prayer). `[SRC]`
- World structure features a set of ceremonial **"Halls" (〜の間)**: 鍛錬の間 (Hall of Forging/Training), 光の間 (Hall of Light), 祈りの間 (Hall of Prayer), 修練の間 (Hall of Discipline), 叡智の間 (Hall of Wisdom), 謁見の間 (Audience Hall), plus the **試練の聖堂** (Sanctuary of Trials). `[SRC]`
- Dungeons are **directional caves**: 東/西/南/北の洞窟 (East/West/South/North Caves) + 秘密の洞穴【1-3】 (Secret Caverns). `[SRC]`
- Notable named places: **エルダーツリー** (Elder Tree), **グランドツリー** (Grand Tree), **ドラゴンピラー** (Dragon Pillar). `[SRC]`

## Tone
- Warm, adventurous, lightly heroic fantasy. `[OFF]`
- Source shows energetic, casual spoken dialogue with frequent exclamations and emotive fragments: うん！ (yeah!), はい！ (yes!), おおー！！！ (oooh!), くっ……！ (ugh!), ん？ (hm?), すぅ……すぅ…… (sleeping breaths). Register is conversational, not archaic. `[SRC]`
- A recurring light/cute motif around cats: ネコ (×212), e.g. "ネコ好きの旅人" (a cat-loving traveler). `[SRC][INF]`

## Major characters (by frequency in source text)
| Source (JP) | Reading (phonetic; verify) | Notes |
|-------------|----------------------------|-------|
| エリオット | **Elliot** `[OFF]` | Protagonist (×872) |
| フェイ | **Faie** `[OFF]` | Fairy partner (×219) |
| マオ | Mao | ×421 — major (often addressed: マオ……) |
| ミュー | Myu / Mew | ×281 |
| ヒューリア | Hyuria | ×276 — major (addressed: ヒューリア……) |
| ヒューリック | Hyurik | ×206 |
| カーター | Carter | ×157 |
| リュドミラ | Lyudmila | ×153 |
| カイフリード | Kaifried | ×119 |
| ディオナ | Diona | ×83 |
| ヒルク | Hilk | ×80 |
| イカロス | Icarus | ×74 |
| ヒルデブラント | Hildebrandt | ×66 — (plot flag seen: "ヒルデブラント生存" = Hildebrandt survives) |
| ユイジーヌ | Eugène? (verify) | ×62 |
| ファウスタ | Fausta | ×52 |
| レイカ | Reika | ×45 |
| マーニー | Marnie | ×41 |
| オリバー | Oliver | ×30 |
| ヒカルド | Hicardo / Ricardo? | ×29 |
| イチル | Ichiru | ×27 |

> `ワタシ` (katakana "I", ×206) recurring suggests a specific character/creature speech style. `[INF]`

## Factions / groups
- `[?]` Not yet clearly identifiable from strings alone. Candidate proper-noun groups/regions to investigate: **フォザワール**, **ラーウェイ**, **カロテシア**, **ディマイズ**, **フォマニット** (could be places, clans, or characters). `[SRC][?]`

## Recurring concepts / terminology
- **魔法** magic (×638) · **魔石** "magicite"/magic-stone (×122; "装備中の魔石" = equipped magic-stone) · **魔獣** magic-beast/monster (×46; "憎悪の魔獣" = beast of hatred). `[SRC]`
- **ライトスタッフ / LightStaff** (×25) — appears in-text; also the internal project codename. `[SRC]`
- Combat actions surfaced as IDs: CircularSawAttack, BodyFallAttack, etc. `[SRC]`
- 7 weapon types (combat) + shield: 剣 Sword, 槍 Spear, 爆弾 Bomb, ブーメラン Boomerang, 鎖 Chain, ハンマー Hammer, 弓 Bow; 盾 Shield (defense). `[SRC][OFF]`

## Relationship / narrative clues
- Dialogue frequently addresses マオ and ヒューリア by name — likely close companions/party to Elliot. `[INF]`
- Ending/credits data references multiple endings (ED1/ED2/ED3) and a branch on **ヒルデブラント生存** (whether Hildebrandt survives) — implies **branching outcomes**. `[SRC]`
- Time-travel premise links the four ages narratively (a "thousand-year mission"). `[OFF]`

## Terminology / formatting patterns (for translators)
- Source uses inline **rich-text markup** that must be preserved: `<cf>` (color/emphasis open), `</>` (close), `<img id="RI_ICON_WPN_*"/>` weapon icons, `<btn id="..."/>` button glyphs. `[SRC]`
- `\n` line breaks pace text boxes; placeholders `{0}{1}{2}{3}` inject values. `[SRC]`
- Tutorials reference 『システム＞設定』 (System > Settings) menu paths in 『』 brackets. `[SRC]`

## PLOT SYNOPSIS `[SRC — reconstructed from the ordered main-story dialogue, chapters M01–M06]`
> Reconstructed by reading the dialogue in scene order (`dialogue_scenes.md`). Names/spellings phonetic where unverified. Minor branch details may vary.

**World.** **フィレビルディア (Philebildia)** — a world after the age of myth. Monstrous **蛮族 ("savage tribes")** roam the wilds fighting over territory; humanity survives in the **ヒューザー王国 (Hewser Kingdom)**, shielded by the **加護 (blessing) magic of Princess ヒューリア (Hyuria)**, who bears that burden almost alone.

**Frame / prologue (M01_E01).** A **future Elliot**, using the power of the firebird **クレイドル (Cradle)**, creates the fairy **フェイ (Faie)** and sends her back in time to aid his younger self, because the seal on the **破壊の竜ディマイズ (Dimaize, the Dragon of Destruction)** is breaking. His dying plea: ally with the clan that governs the seal, defeat the dragon, save the kingdom — and he entrusts a keepsake.

**Hero.** **Elliot (PCM000)** — a kind, humble adventurer, found as a baby 20 years ago beneath the **Elder Tree**, cradled by a dead stranger (his presumed father); named for the tree. Raised in an orphanage he now supports, alongside matron **レイカ (Reika)**. Specialist in the dangerous lands outside the kingdom.

**Inciting story (M01).** Scholar **ユイジーヌ (Eugène)**, Elliot's old friend, recommends him to **King ヒカルド (Hicardo)** — who follows the Hero King's creed *"do not be ruled by power; those who crave power are destroyed by it,"* against his militaristic retainer **カイフリード (Kaifried)**. Elliot is sent to investigate newly-found ruins for lost magic that might ease Hyuria's burden. Hyuria, longing to see the outside world, enchants Elliot's earring to support him remotely and joins as his partner (later, the time-fairy **Faie** becomes his companion). Deep in the ruins they find a **mysterious great door** — the **時の扉 (Door of Time)**.

**Journey (M02–M05).** Through the Door, Elliot travels the **four ages** — 始まり (Beginning), 魔法 (Magic), 再建 (Reconstruction), 加護 (Blessing) — allying with the **ミュー族 (Mew tribe)** and the **三賢者 (Three Sages)**, gathering the means to face the dragon. Along the way he uncovers his own origins, including his mother **ラーウェイ (Rāwei)**.

**Climax (M06).** The seal breaks and Dimaize awakens. The Sages channel magic to **revive the firebird Cradle**; Elliot rides it into the final battle. Carried by the combined will of Hyuria, his mother Rāwei, Faie, and the Sages, he defeats Dimaize (Faie is briefly devoured but survives). The future is rewritten — **humans and the Mew tribe living together.**

**Ending.** In a liminal space, **future Elliot** contacts Faie, thanks her, and tells her the future is changed; Faie chooses to **stay in the present** beside young Elliot to watch over him. Cradle blesses them both: *"Hope is always by your side."* (Matches the tagline **"Hope is timeless."**) A branch flag (**Hildebrandt survives**) reflects player-choice ending variants.

**Themes / tone.** Hope, found family, sacrifice, changing the future, coexistence. Warm and heroic with genuine emotional beats and recurring light humor (the mischievous cat / Mew motif, Faie's childlike energy).

## Character voices / registers `[SRC]` (for Arabic register + gender agreement)
> The `speaker`/`speaker_gender` fields are now in `01_extracted_strings.jsonl` (decoded from keys). Match each voice:
- **Elliot (PCM000, male)** — warm, easygoing, modest; jokes gently; speaks plainly to friends, politely to royalty.
- **Hyuria (NPC0010, female)** — polite/refined princess (です・ます), earnest and kind; addresses Elliot by name.
- **Faie (the fairy, female; self-refers ワタシ)** — childlike, bubbly, devoted; casual and energetic.
- **King Hicardo (NPC0030, male)** — archaic/regal register (余, ひかえよ); dignified.
- **Kaifried (NPC0040, male)** — stiff, militaristic, brusque.
- **Eugène (NPC0020, male)** — measured, clever scholar.
- **Orphanage children (NPC43xx)** — childish, affectionate, simple speech.
- **Cradle the firebird (NPC9000, female)** — solemn, ancient, oracular.

## Uncertainty notes
- Romanizations of minor characters/places are phonetic and **unverified** vs. official English. `[?]`
- Factions, exact plot, and character relationships are **inferred** from term frequency and fragments, not confirmed narrative. `[INF][?]`
- ~50–100 source entries are corrupted (mojibake) and excluded from analysis (see `03`). `[SRC]`
- English official text (a useful cross-check) was **not** extracted yet (deferred to QA per project decision).
