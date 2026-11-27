# gbf_tani/assets.py
"""
Semua path template gambar di satu tempat.
Path relatif terhadap root project (bot dijalankan dari folder yang berisi main.py).
"""

# === Tombol ===
BTN_ATTACK = "assets/button/attack.png"
BTN_AUTO = "assets/button/auto.png"
BTN_BACK = "assets/button/back.png"
BTN_BATTLE_END = "assets/button/battle_end.png"
BTN_BATTLE_END_TIME = "assets/button/battle_end_time.png"
BTN_BOOKMARK = "assets/button/bookmark.png"
BTN_DEAD = "assets/button/dead.png"
BTN_DROP_ITEMS = "assets/button/drop_items.png"
BTN_FINDER = "assets/button/finder.png"
BTN_FINDER_ACTIVE = "assets/button/finder_active.png"
BTN_OK = "assets/button/button_ok.png"
BTN_QUICK_SUMMON = "assets/button/quick_summon.png"
BTN_QUICK_SUMMON_2 = "assets/button/quick_summon2.png"
BTN_REFRESH = "assets/button/refresh.png"
BTN_RELOAD = "assets/button/reload.png"

# === Halaman / popup ===
PAGE_BACKUP_REQUESTS = "assets/page/backup_requests.png"
PAGE_SOLO = "assets/page/page_solo.png"
PAGE_SENBOK = "assets/page/senbok.png"
PAGE_IN_BATTLE = "assets/page/in_battle.png"
PAGE_RESULT_BATTLE = "assets/page/img_result_battle.png"
PAGE_RESULT_BATTLE_2 = "assets/page/img_result_battle_2.png"
PAGE_EXP_GAINED = "assets/page/exp_gained.png"
PAGE_PARTY_WIPE = "assets/page/party_wipe.png"
PAGE_CAPTCHA = "assets/page/captcha.png"
PAGE_PENDING_BATTLE = "assets/page/img_pending_battle.png"
PAGE_RAID_BATTLE_ENDED = "assets/page/img_raid_battle_ended.png"
PAGE_RAID_BATTLE_FULL = "assets/page/img_raid_battle_full.png"
PAGE_POPUP = "assets/page/popup.png"

# === Party ===
PARTY_DIR = "assets/party"
PARTY_HEAL = "assets/party/heal.png"
PARTY_SKILL_BAR = "assets/party/skill.png"
PARTY_SUMMON = "assets/party/summon.png"

# Template result battle, urutan dicek sesuai urutan list
RESULT_SCREENS = (PAGE_RESULT_BATTLE, PAGE_RESULT_BATTLE_2)
RESULT_SCREENS_WITH_EXP = (PAGE_RESULT_BATTLE, PAGE_RESULT_BATTLE_2, PAGE_EXP_GAINED)

# Tanda battle berakhir saat nunggu tombol attack hilang (urutan dicek)
BATTLE_END_SIGNS = (BTN_BATTLE_END, BTN_BATTLE_END_TIME, BTN_DEAD, PAGE_PARTY_WIPE)


def party_slot(position):
    """Template karakter party, contoh: party_slot("1st") → assets/party/1st.png"""
    return f"{PARTY_DIR}/{position}.png"
