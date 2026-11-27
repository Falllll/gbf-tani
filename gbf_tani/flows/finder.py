# gbf_tani/flows/finder.py
import sys
import time

from gbf_tani import assets
from gbf_tani.config import raid_source, raid_name
from gbf_tani.flows.battle import handle_battle
from gbf_tani.flows.pending_battle import handling_pending_battle
from gbf_tani.game.buttons import button_refresh, button_reload, button_bookmark, click_bookmark
from gbf_tani.game.popups import (
    check_captcha,
    check_common_popups,
    check_pending_battle,
    check_select_summon,
    handle_common_popup_action,
    is_battle_result,
)
from gbf_tani.vision.capture import screenshot
from gbf_tani.vision.matcher import match_template
from gbf_tani.vision.mouse import click_coords, click_image

MAX_FAIL = 10


def select_raid():
    """
    Cari raid (raid_source dari data.json) di tab Finder, join, lalu battle.
    Return:
        True  -> battle selesai (result muncul)
        False -> gagal / popup, caller ulangi dari awal
    CAPTCHA → program berhenti.
    """
    if not raid_source:
        print("❌ raid_source tidak ditemukan di data.json/config.json")
        return False

    print(f"🔍 Mulai cari raid {raid_name}")
    fail_count = 0

    while True:
        coords = match_template(screenshot(), raid_source, threshold=0.6, return_coords=True, preprocess=True)

        if not coords:
            button_refresh()

            if (result := _check_join_popups(after_summon=False)) is not None:
                return result

            fail_count += 1
            print(f"⚠️ Raid tidak dikenali (percobaan {fail_count}/{MAX_FAIL}), ulangi…")
            time.sleep(2)
            if fail_count >= MAX_FAIL:
                print("❌ Raid gagal terdeteksi 10x → reload + bookmark.")
                button_reload()
                time.sleep(0.5)
                button_bookmark()
                fail_count = 0
            continue

        # --- Raid ketemu → join ---
        fail_count = 0
        cx, cy, _ = coords
        print("✅ Raid ditemukan, memilih raid…")
        time.sleep(0.5)
        click_coords(cx, cy)
        time.sleep(1)

        if (result := _check_join_popups(after_summon=False)) is not None:
            return result

        # --- Pilih summon ---
        time.sleep(1)
        if not check_select_summon():
            return False

        print("✅ Klik OK")
        click_image(assets.BTN_OK, threshold=0.7)
        time.sleep(1.5)

        result = _check_join_popups(after_summon=True)
        if result == "retry":
            continue
        if result is not None:
            return result

        # --- Battle ---
        if is_battle_result(screenshot(), threshold=0.6):
            print("✅ Battle selesai, result screen muncul")
            click_bookmark()
            return True

        handle_battle()


def _check_join_popups(after_summon):
    """
    Cek popup setelah klik raid / setelah OK summon.
    Return:
        None    -> aman, lanjut
        False   -> popup / pending battle, caller return False
        "retry" -> (setelah summon) pending battle sudah di-handle, ulangi loop
    """
    popup_screen = screenshot()
    print("✅ Check Pop up setelah summon OK" if after_summon else "✅ Check Pop up")

    popup_name = check_common_popups(popup_screen)
    if popup_name:
        if after_summon:
            print(f"⚠️ Popup terdeteksi setelah summon OK: {popup_name}")
            button_bookmark()
            return False
        return handle_common_popup_action(popup_name)

    if check_pending_battle(popup_screen):
        if after_summon:
            print("⚠️ Pending battle setelah summon OK → menjalankan handler.")
            handling_pending_battle()
            return "retry"
        print("⚠️ Pending battle terdeteksi → menjalankan handler.")
        handling_pending_battle()
        return False

    if after_summon and check_captcha(popup_screen):
        print("⚠️ CAPTCHA TERDETEKSI → hentikan program.")
        sys.exit()

    return None
