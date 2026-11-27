# gbf_tani/flows/navigator.py
"""Pastikan bot ada di halaman yang benar untuk mode yang dipilih, lalu jalankan alurnya."""
import time

from gbf_tani import assets, session
from gbf_tani.flows.battle import run_battle
from gbf_tani.flows.finder import select_raid
from gbf_tani.game.buttons import click_ok_button, reset_to_bookmark, wait_for_auto_button
from gbf_tani.game.popups import check_captcha
from gbf_tani.vision.capture import screenshot
from gbf_tani.vision.matcher import match_template
from gbf_tani.vision.mouse import click_image
from gbf_tani.log import log

MAX_ATTEMPT = 10


def check_tab(mode: str) -> bool:
    """Satu putaran bot sesuai mode: "finder" atau "solo"."""
    if mode == "finder":
        raid_page()
        return False
    if mode == "solo":
        return solo_page()
    return False


# ---------------------------------------------------------------------------
# Mode solo
# ---------------------------------------------------------------------------

def solo_page():
    attempt = 0
    while True:
        screen = screenshot()

        if match_template(screen, assets.PAGE_SOLO, preprocess=False):
            log("✅ Sudah di halaman solo")
            _start_solo_battle()
            return True

        if match_template(screen, assets.PAGE_SENBOK, preprocess=False):
            log("✅ Sudah di halaman senbok")
            return True

        if match_template(screen, assets.PAGE_IN_BATTLE, preprocess=False):
            log("✅ Sudah di halaman battle, jalankan battle")
            run_battle()
            return True

        attempt += 1
        log(f"❌ Harus ada di halaman solo (percobaan {attempt})")
        attempt = _reset_if_max(attempt)
        time.sleep(2)


def _start_solo_battle():
    """Klik OK di halaman solo, cek captcha, tunggu tombol auto, lalu battle (FA / manual)."""
    click_ok_button()
    time.sleep(0.5)

    if check_captcha(screenshot()):
        session.stop_for_captcha()

    if wait_for_auto_button(timeout=30, interval=0.5, debug=False):
        run_battle()
    else:
        log("⚠️ Tombol auto tidak muncul setelah klik OK")


# ---------------------------------------------------------------------------
# Mode finder
# ---------------------------------------------------------------------------

def raid_page():
    """Pastikan di halaman backup request + tab Finder, lalu select_raid()."""
    attempt = 0
    while True:
        if not match_template(screenshot(), assets.PAGE_BACKUP_REQUESTS, preprocess=False):
            log("❌ Harus ada di halaman backup raid")
            time.sleep(2)
            attempt += 1
            log(f"⚠️ Percobaan gagal ke-{attempt}/{MAX_ATTEMPT}")
            attempt = _reset_if_max(attempt)
            continue

        log("✅ Sudah di halaman backup")
        log("ℹ️ Cek apakah sudah di tab finder jika belum, pindah tab...")

        if _open_finder_tab():
            return select_raid()

        log("❌ Gagal menemukan tombol Finder")
        attempt += 1
        log(f"⚠️ Percobaan gagal ke-{attempt}/{MAX_ATTEMPT}")
        attempt = _reset_if_max(attempt)


def _open_finder_tab():
    """Coba 3x pastikan tab Finder aktif. Return True kalau berhasil."""
    for _ in range(3):
        screen = screenshot()

        if match_template(screen, assets.BTN_FINDER_ACTIVE, threshold=0.4, preprocess=True):
            log("✅ Sudah di tab Finder (aktif)")
            return True

        if match_template(screen, assets.BTN_FINDER, threshold=0.4, preprocess=True):
            click_image(assets.BTN_FINDER, threshold=0.4)
            time.sleep(1)
            log("✅ Berhasil pindah ke tab Finder")
            return True

        time.sleep(0.5)
    return False


def _reset_if_max(attempt):
    """Kalau gagal sudah MAX_ATTEMPT kali → reload + bookmark, counter balik 0."""
    if attempt < MAX_ATTEMPT:
        return attempt
    log(f"🔄 {MAX_ATTEMPT}x gagal, klik bookmark untuk reset")
    reset_to_bookmark()
    return 0
