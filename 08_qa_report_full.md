# 08 — QA Report

Rows checked: **4776**  |  Total issues: **28**

## [HIGH] Same source, inconsistent Arabic — 7

| ID | Detail |
|----|--------|
| - | '……君が最後の希望なんだ。\\nどうか頼む――' -> 2 variants |
| - | '王国を――………………救ってくれ……！' -> 2 variants |
| - | 'はっ！' -> 2 variants |
| - | '任された。\\n旅の無事を祈ってるよ。' -> 2 variants |
| - | 'がんばってね、あんちゃん！' -> 2 variants |
| - | 'う、うう……' -> 2 variants |
| - | 'う……うう……' -> 2 variants |

## [MEDIUM] Dialectal Arabic (should be MSA) — 1

| ID | Detail |
|----|--------|
| EL_BONUS_TITLE_3_NAME | dialectal marker 'دي' (use MSA) |

## [MEDIUM] UI string too long — 19

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
| EL_Tutorial_GameSetting_01_1_Title | 29 chars (>28) |
| EL_Tutorial_GameSetting_01_Title | 29 chars (>28) |

## [LOW] Target suspiciously long vs source — 1

| ID | Detail |
|----|--------|
| EL_RECORD_14 | target 41 vs source 10 |
