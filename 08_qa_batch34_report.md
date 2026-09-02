# 08 — QA Report

Rows checked: **4287**  |  Total issues: **123**

## [CRITICAL] Missing placeholders/tags — 8

| ID | Detail |
|----|--------|
| EL_MAGICSTONE_BOOMERANG_08_DESCRIPTION | missing ['\\n'] |
| EL_MAGICSTONE_SWORD_05_DESCRIPTION | missing ['\\n'] |
| EL_M01_E10_1000_M050_NPC0020_m | missing ['\\n'] |
| EL_M01_E10_1000_M170_NPC0010_f | missing ['\\n'] |
| EL_M01_E12_1000_M230_NPC0010_f | missing ['\\n'] |
| EL_M01_E12_2000_M110_NPC0020_m | missing ['\\n'] |
| EL_M01_E12_2000_M190_PCM000_m | missing ['\\n'] |
| EL_M01_E12_2000_M230_NPC0010_f | missing ['\\n'] |

## [CRITICAL] Added/extra placeholders — 6

| ID | Detail |
|----|--------|
| EL_SYSTEM_Tutorial | extra ['\\n'] |
| EL_ABFCC3EA4672D1845555E4AC4C6B8DB4 | extra ['\\n'] |
| EL_ITEM_Important | extra ['\\n'] |
| EL_QUEST_Sub | extra ['\\n'] |
| EL_S04_N29_3000_M110_PCM000_m | extra ['\\n'] |
| EL_SPPLAY_ITEMGET_T21_A_M01_NPC0010_f | extra ['\\n', '\\n'] |

## [HIGH] Newline count mismatch — 4

| ID | Detail |
|----|--------|
| EL_SYSTEM_Tutorial | newline delta -1 |
| EL_ABFCC3EA4672D1845555E4AC4C6B8DB4 | newline delta -1 |
| EL_ITEM_Important | newline delta -1 |
| EL_QUEST_Sub | newline delta -1 |

## [HIGH] No Arabic script in target — 1

| ID | Detail |
|----|--------|
| EL_A9_TITLE_2_NAME | target has no Arabic letters |

## [HIGH] Same source, inconsistent Arabic — 10

| ID | Detail |
|----|--------|
| - | 'バケネコに対してダメージを与え続けるエリオット\\nバケネコはさらに魔力を強める' -> 2 variants |
| - | '"・体力が{Num:1}％以下の敵に対し、\\n\u3000<img id=""RI_ICO' -> 2 variants |
| - | '"・<img id=""RI_ICON_WPN_SWORD""/>のダメージが{' -> 2 variants |
| - | '"・盾の耐久力が{Num:1}％以上の時、\\n\u3000<img id=""RI_ICO' -> 2 variants |
| - | '依頼を果たしたエリオットは店主から\\n岩を壊すための爆弾を受け取る。' -> 2 variants |
| - | '……わかりました。' -> 2 variants |
| - | '……わかりました。\\n私も協力いたしましょう。' -> 2 variants |
| - | 'ヒューリア様……？' -> 2 variants |
| - | '『希望は、いつも“そこ”にある』' -> 2 variants |
| - | 'はっ！' -> 2 variants |

## [MEDIUM] Glossary term not applied — 41

| ID | Detail |
|----|--------|
| EL_2D5993984C08D4F28F72DA92970A697A | 'ネコ探知の針' expected 'إبرة تعقب القطط' |
| EL_2D5993984C08D4F28F72DA92970A697A | 'ネコ探知の針' expected 'إبرة تعقب القطط' |
| EL_BOS410 | '憎悪の魔獣' expected 'الوحش السحري المكروه' |
| EL_BOS410 | '憎悪の魔獣' expected 'الوحش السحري المكروه' |
| EL_BOS410_ED02 | '憎悪の魔獣' expected 'الوحش السحري المكروه' |
| EL_BOS410_ED02 | '憎悪の魔獣' expected 'الوحش السحري المكروه' |
| EL_BOS410_ED03 | '憎悪の魔獣' expected 'الوحش السحري المكروه' |
| EL_BOS410_ED03 | '憎悪の魔獣' expected 'الوحش السحري المكروه' |
| EL_BOS411 | '憎悪の魔獣' expected 'الوحش السحري المكروه' |
| EL_BOS411 | '憎悪の魔獣' expected 'الوحش السحري المكروه' |
| EL_COMPASS_NEEDLE_4_NAME | 'ネコ探知の針' expected 'إبرة تعقب القطط' |
| EL_COMPASS_NEEDLE_4_NAME | 'ネコ探知の針' expected 'إبرة تعقب القطط' |
| EL_ITEM_CONTAINER_ATK_NAME | '闘志の薬' expected 'جرعة الروح القتالية' |
| EL_ITEM_CONTAINER_ATK_NAME | '闘志の薬' expected 'جرعة الروح القتالية' |
| EL_M06_E03_2000_Title | '憎悪の魔獣' expected 'الوحش السحري المكروه' |
| EL_M06_E03_2000_Title | '憎悪の魔獣' expected 'الوحش السحري المكروه' |
| EL_NPC4019 | 'ロウエル' expected 'رولل' |
| EL_NPC4019 | 'ロウエル' expected 'رولل' |
| EL_WPN_COMPASS_NAME | '魔力コンパス' expected 'بوصلة القوة السحرية' |
| EL_WPN_COMPASS_NAME | '魔力コンパス' expected 'بوصلة القوة السحرية' |
| EL_Area_Shop_A3 | 'マギーのよろず屋' expected 'متجر ماغي المتنوع' |
| EL_Area_Shop_A3 | 'マギーのよろず屋' expected 'متجر ماغي المتنوع' |
| EL_SPPLAY_BTL_A13_C_M01_FYL000_f | '魔石' expected 'حجر السحر' |
| EL_WPN_BOMB_1_DESCRIPTION | '攻撃力' expected 'الهجوم' |
| EL_WPN_BOOMERANG_1_DESCRIPTION | '攻撃力' expected 'الهجوم' |
| EL_WPN_BOOMERANG_2_DESCRIPTION | '攻撃力' expected 'الهجوم' |
| EL_WPN_BOOMERANG_3_DESCRIPTION | '攻撃力' expected 'الهجوم' |
| EL_WPN_BOW_1_DESCRIPTION | '攻撃力' expected 'الهجوم' |
| EL_WPN_BOW_2_DESCRIPTION | '攻撃力' expected 'الهجوم' |
| EL_WPN_BOW_3_DESCRIPTION | '攻撃力' expected 'الهجوم' |
| EL_WPN_CHAIN_1_DESCRIPTION | '攻撃力' expected 'الهجوم' |
| EL_WPN_CHAIN_2_DESCRIPTION | '攻撃力' expected 'الهجوم' |
| EL_WPN_CHAIN_3_DESCRIPTION | '攻撃力' expected 'الهجوم' |
| EL_WPN_HAMMER_1_DESCRIPTION | '攻撃力' expected 'الهجوم' |
| EL_WPN_HAMMER_2_DESCRIPTION | '攻撃力' expected 'الهجوم' |
| EL_WPN_HAMMER_3_DESCRIPTION | '攻撃力' expected 'الهجوم' |
| EL_WPN_SPEAR_1_DESCRIPTION | '攻撃力' expected 'الهجوم' |
| EL_WPN_SPEAR_2_DESCRIPTION | '攻撃力' expected 'الهجوم' |
| EL_WPN_SPEAR_3_DESCRIPTION | '攻撃力' expected 'الهجوم' |
| EL_WPN_SWORD_1_DESCRIPTION | '攻撃力' expected 'الهجوم' |
| EL_WPN_SWORD_2_DESCRIPTION | '攻撃力' expected 'الهجوم' |

## [MEDIUM] UI string too long — 20

| ID | Detail |
|----|--------|
| EL_6E903F704B8D134F41CBF588EA6DB778 | 38 chars (>28) |
| EL_Area_Last | 29 chars (>28) |
| EL_BC5E39EA42ABED266025658C236B5804 | 41 chars (>28) |
| EL_M01_E08_1000_01 | 33 chars (>28) |
| EL_M01_E09_1000_Title | 29 chars (>28) |
| EL_M04_E15_3000 | 111 chars (>28) |
| EL_M05_A1MGC_E01_1000_M030_NPC0200_m | 101 chars (>28) |
| EL_M06_E04_1000 | 122 chars (>28) |
| EL_MainMenuSystemApplyDialog | 47 chars (>28) |
| EL_MainMenuSystemDscNSWGraphicModeGraph | 59 chars (>28) |
| EL_MainMenuSystemMsgVSyncExp | 32 chars (>28) |
| EL_MainMenuSystemTextModel | 36 chars (>28) |
| EL_MainMenuSystemTitleMsgPresetCustomExp | 36 chars (>28) |
| EL_RECORD_14 | 41 chars (>28) |
| EL_S03_N28_1000_04_C01_txt01 | 29 chars (>28) |
| EL_SP02_LAST_A3_BOSS_KEY_NAME | 33 chars (>28) |
| EL_SP02_LAST_A4_KEY_NAME | 33 chars (>28) |
| EL_SYSTEM_Tutorial | 60 chars (>28) |
| EL_Tutorial_GameSetting_01_1_Title | 29 chars (>28) |
| EL_Tutorial_GameSetting_01_Title | 29 chars (>28) |

## [LOW] Target suspiciously long vs source — 26

| ID | Detail |
|----|--------|
| EL_RECORD_14 | target 41 vs source 10 |
| EL_S04_N29_3000_M110_PCM000_m | target 238 vs source 28 |
| EL_SPPLAY_ITEMGET_T21_A_M01_NPC0010_f | target 447 vs source 26 |
| EL_Tutorial_Hammer_01_1_Text | target 86 vs source 20 |
| EL_Tutorial_MagicStoneShop_01b_1_Title | target 95 vs source 14 |
| EL_Tutorial_MagicStoneShop_01b_Title | target 95 vs source 14 |
| EL_Tutorial_Shop_01_1_Title | target 100 vs source 10 |
| EL_Tutorial_Shop_01_Title | target 100 vs source 10 |
| EL_WPN_BOMB_1_DESCRIPTION | target 63 vs source 11 |
| EL_WPN_BOOMERANG_1_DESCRIPTION | target 63 vs source 11 |
| EL_WPN_BOOMERANG_2_DESCRIPTION | target 63 vs source 11 |
| EL_WPN_BOOMERANG_3_DESCRIPTION | target 63 vs source 11 |
| EL_WPN_BOW_1_DESCRIPTION | target 63 vs source 11 |
| EL_WPN_BOW_2_DESCRIPTION | target 63 vs source 11 |
| EL_WPN_BOW_3_DESCRIPTION | target 63 vs source 11 |
| EL_WPN_CHAIN_1_DESCRIPTION | target 63 vs source 11 |
| EL_WPN_CHAIN_2_DESCRIPTION | target 63 vs source 11 |
| EL_WPN_CHAIN_3_DESCRIPTION | target 63 vs source 11 |
| EL_WPN_HAMMER_1_DESCRIPTION | target 63 vs source 11 |
| EL_WPN_HAMMER_2_DESCRIPTION | target 63 vs source 11 |
| EL_WPN_HAMMER_3_DESCRIPTION | target 63 vs source 11 |
| EL_WPN_SPEAR_1_DESCRIPTION | target 63 vs source 11 |
| EL_WPN_SPEAR_2_DESCRIPTION | target 63 vs source 11 |
| EL_WPN_SPEAR_3_DESCRIPTION | target 63 vs source 11 |
| EL_WPN_SWORD_1_DESCRIPTION | target 63 vs source 11 |
| EL_WPN_SWORD_2_DESCRIPTION | target 63 vs source 11 |

## [MEDIUM] ASCII punctuation instead of Arabic — 7

| ID | Detail |
|----|--------|
| EL_ABFCC3EA4672D1845555E4AC4C6B8DB4 | ',' should be '،' |
| EL_ITEM_Important | ',' should be '،' |
| EL_S04_N29_3000_M110_PCM000_m | ',' should be '،' |
| EL_SPPLAY_ITEMGET_T21_A_M01_NPC0010_f | ',' should be '،' |
| EL_Tutorial_Hammer_01_1_Text | ',' should be '،' |
| EL_Tutorial_MagicStoneFay_01_1_Title | ',' should be '،' |
| EL_Tutorial_MagicStoneFay_01_Title | ',' should be '،' |
