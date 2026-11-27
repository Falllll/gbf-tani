# gbf_tani/game/popups.py
import time

from gbf_tani import assets
from gbf_tani.game.buttons import reload_then_bookmark
from gbf_tani.vision.capture import screenshot
from gbf_tani.vision.matcher import match_template, match_any

# Popup umum setelah join raid (urutan dicek sesuai urutan dict)
COMMON_POPUPS = {
    "battle_ended": assets.PAGE_RAID_BATTLE_ENDED,
    "backup_3": assets.PAGE_POPUP,
    "battle_full": assets.PAGE_RAID_BATTLE_FULL,
}


def check_common_popups(screen, threshold=0.6):
    """Return nama popup yang terdeteksi, None kalau tidak ada."""
    for name, img in COMMON_POPUPS.items():
        if match_template(screen, img, threshold=threshold, preprocess=True):
            return name
    return None


def handle_common_popup_action(name):
    """Popup umum → reload + bookmark, return False supaya caller ulang dari awal."""
    print(f"⚠️ Popup terdeteksi: {name}")
    reload_then_bookmark(delay=0.3)
    return False


def check_pending_battle(screen):
    return match_template(screen, assets.PAGE_PENDING_BATTLE, threshold=0.35, preprocess=True)


def check_captcha(screen):
    return match_template(screen, assets.PAGE_CAPTCHA, threshold=0.6, preprocess=True)


def is_battle_result(screen, threshold, with_exp=False):
    """Cek layar result battle (opsional termasuk layar EXP gained)."""
    templates = assets.RESULT_SCREENS_WITH_EXP if with_exp else assets.RESULT_SCREENS
    return match_any(screen, templates, threshold=threshold, preprocess=True)


def check_select_summon():
    """
    Sekali cek apakah sudah di halaman select summon.
    Kalau belum → reload + bookmark, return False.
    """
    screen = screenshot()
    if match_template(screen, assets.BTN_DROP_ITEMS, preprocess=False):
        print("✅ Sudah di halaman select summon")
        return True

    print("❌ Tidak berada di halaman select summon, balik bookmark...")
    reload_then_bookmark(delay=0.3)
    time.sleep(1)
    return False
