# gbf_tani/flows/pending_battle.py
import time

from gbf_tani import assets
from gbf_tani.config import raid_source
from gbf_tani.game.buttons import button_reload, click_bookmark, click_back
from gbf_tani.game.popups import is_battle_result
from gbf_tani.vision.capture import screenshot
from gbf_tani.vision.matcher import match_template
from gbf_tani.vision.mouse import click_box, click_image
from gbf_tani.log import log

RESULT_WAIT_SECONDS = 10


def handling_pending_battle():
    """
    Popup pending battle → klik OK, lalu buka raid pending satu per satu
    sampai tidak ada lagi. Return True kalau bersih, False kalau result tidak muncul.
    """
    log("⚠️ Handling pending battle...")

    click_image(assets.BTN_OK, threshold=0.7)
    time.sleep(1)

    while True:
        coords = match_template(screenshot(), raid_source, threshold=0.4, return_coords=True, preprocess=True)

        if not coords:
            log("✅ Tidak ada raid pending lagi, keluar dari handling_pending_battle")
            click_bookmark()
            return True

        time.sleep(0.1)
        log(f"➡️ Klik raid pending (score={coords.score:.3f})")
        click_box(coords.box)
        time.sleep(1)

        if not _wait_result_and_back():
            log("⚠️ Result battle tidak muncul setelah 10 detik, klik bookmark untuk reset")
            button_reload()
            time.sleep(1)
            click_bookmark()
            time.sleep(1)
            return False


def _wait_result_and_back():
    """Tunggu layar result (maks ~10 detik), lalu klik back. Return True kalau ketemu."""
    for _ in range(RESULT_WAIT_SECONDS):
        if is_battle_result(screenshot(), threshold=0.6):
            log("✅ Result battle terdeteksi, klik Back")
            click_back(threshold=0.7)
            time.sleep(2)
            return True
        time.sleep(1)
    return False
