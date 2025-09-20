from utils.screenshot import screenshot, match_template, click_coords, click_image_fullscreen
from core.page_checker import check_select_summon
from utils.config import raid_source, raid_name
from core.button import button_refresh, button_reload, button_bookmark
from core.popup import (
    check_common_popups,
    check_pending_battle,
    check_captcha,
    handle_common_popup_action
)
from core.pending_battle import handling_pending_battle
from core.battle import handle_battle
import time

def select_raid():
    """
    Cari dan pilih raid sesuai raid_source dari data.json.
    Return:
        "captcha"  -> jika CAPTCHA terdeteksi
        True       -> jika raid berhasil dipilih
        False      -> jika gagal, coba ulangi
    """
    if not raid_source:
        print("❌ raid_source tidak ditemukan di data.json/config.json")
        return False

    print(f"🔍 Mulai cari raid {raid_name}")
    fail_count = 0

    while True:
        screen = screenshot()
        coords = match_template(screen, raid_source, threshold=0.6,
                                return_coords=True, preprocess=True)

        if coords:
            fail_count = 0
            cx, cy, score = coords
            print(f"✅ Raid ditemukan, memilih raid…")
            time.sleep(0.5)
            click_coords(cx, cy)
            time.sleep(1)

            popup_screen = screenshot()
            print("✅ Check Pop up")

            popup_name = check_common_popups(popup_screen, debug=True)
            if popup_name:
                return handle_common_popup_action(popup_name)

            if check_pending_battle(popup_screen, debug=True):
                print("⚠️ Pending battle terdeteksi → menjalankan handler.")
                handling_pending_battle(debug=True)
                return False

            # ✅ Lanjut ke summon
            time.sleep(1)
            if not check_select_summon():
                return False

            print("✅ Klik OK")
            click_image_fullscreen("assets/button/button_ok.png", threshold=0.7)

            time.sleep(1.5)
            popup_screen = screenshot()
            print("✅ Check Pop up setelah summon OK")

            popup_name = check_common_popups(popup_screen, debug=True)
            if popup_name:
                print(f"⚠️ Popup terdeteksi setelah summon OK: {popup_name}")
                button_bookmark()
                return False

            if check_pending_battle(popup_screen, debug=True):
                print("⚠️ Pending battle setelah summon OK → menjalankan handler.")
                handling_pending_battle(debug=True)
                continue

            if check_captcha(popup_screen, debug=True):
                print("⚠️ CAPTCHA TERDETEKSI → hentikan program.")
                exit()

            handle_battle()

        else:
            if button_refresh():
                continue
            fail_count += 1
            print(f"⚠️ Raid tidak dikenali (percobaan {fail_count}/10), ulangi…")
            time.sleep(2)
            if fail_count >= 10:
                print("❌ Raid gagal terdeteksi 10x → reload + bookmark.")
                button_reload()
                time.sleep(0.5)
                button_bookmark()
                fail_count = 0
