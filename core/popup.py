from utils.screenshot import match_template, click_image_fullscreen

# Konfigurasi popup umum
POPUPS = {
    "battle_ended": "assets/page/img_raid_battle_ended.png",
    "backup_3": "assets/page/popup.png",
    "battle_full": "assets/page/img_raid_battle_full.png",
}

PENDING_BATTLE_IMG = "assets/page/img_pending_battle.png"
CAPTCHA_IMG = "assets/page/captcha.png"

def check_common_popups(screen, threshold=0.6, debug=False):
    """
    Mengecek popup umum (raid ended, backup 3, battle full).
    Return nama popup jika terdeteksi, None jika tidak ada.
    """
    for name, img in POPUPS.items():
        if match_template(screen, img, threshold=threshold, preprocess=True,
                          reject_dark=False, debug=debug):
            return name
    return None

def check_pending_battle(screen, debug=False):
    """
    Mengecek popup pending battle.
    Return True jika terdeteksi, False jika tidak.
    """
    return match_template(screen, PENDING_BATTLE_IMG, threshold=0.4, preprocess=True,
                          reject_dark=False, debug=debug)

def check_captcha(screen, debug=False):
    """
    Mengecek CAPTCHA.
    Return True jika CAPTCHA terdeteksi, False jika tidak.
    """
    return match_template(screen, CAPTCHA_IMG, threshold=0.5, preprocess=True,
                          reject_dark=False, debug=debug)

def handle_common_popup_action(name):
    """
    Aksi default saat popup umum terdeteksi.
    Klik reload + bookmark lalu return False untuk mengulang loop.
    """
    print(f"⚠️ Popup terdeteksi: {name}")
    click_image_fullscreen("assets/button/reload.png", threshold=0.7)
    click_image_fullscreen("assets/button/bookmark.png", threshold=0.7)
    return False
