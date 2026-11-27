# gbf_tani/flows/battle.py
import random
import time

from gbf_tani import assets
from gbf_tani.config import fast_refresh, full_auto, raid_intro
from gbf_tani.flows.manual import manual
from gbf_tani.game.buttons import button_reload, click_bookmark, click_back
from gbf_tani.game.popups import is_battle_result
from gbf_tani.vision.capture import screenshot
from gbf_tani.vision.matcher import match_template
from gbf_tani.vision.mouse import click_image
from gbf_tani.log import log

ATTACK_WAIT_TIMEOUT = 60  # detik

# fast_refresh: jeda acak (detik) setelah klik auto, lalu langsung klik back
FAST_REFRESH_MIN, FAST_REFRESH_MAX = 0.5, 1.0


def handle_battle():
    """Masuk battle dari finder → lewati intro raid (kalau ada), lalu run_battle()."""
    time.sleep(0.5)
    if raid_intro:
        button_reload()

    run_battle()


def run_battle():
    """Jalankan battle sesuai config: full auto atau manual (manual.json). Dipakai finder & solo."""
    if full_auto:
        fa()
    else:
        manual()


def fa():
    """
    Full auto:
    1. Result screen muncul → bookmark, selesai.
    2. Tombol auto tidak ada → hitung gagal (maks 10x), cek result / party wipe.
    3. Tombol auto ada → klik, tunggu tombol attack hilang, klik back, ulangi.
    """
    fail_count = 0
    while True:
        screen = screenshot()

        if is_battle_result(screen, threshold=0.7):
            log("✅ Battle selesai, result screen muncul")
            click_bookmark()
            return True

        coords_auto = match_template(screen, assets.BTN_AUTO, threshold=0.5, return_coords=True, preprocess=True)
        if not coords_auto:
            fail_count += 1
            log(f"⚠️ Tombol auto tidak ditemukan ({fail_count}/10)")
            time.sleep(1)

            if is_battle_result(screen, threshold=0.6):
                log("✅ Battle selesai, result screen muncul")
                click_bookmark()
                return True

            if match_template(screen, assets.BTN_DEAD, threshold=0.5, preprocess=True):
                log("⚠️ Party wipe")
                click_bookmark()
                return True

            if fail_count >= 10:
                log("❌ Auto gagal ditemukan 10x, klik bookmark lalu keluar")
                click_bookmark()
                return True

            continue

        fail_count = 0
        log("✅ Tombol auto ditemukan → klik sekali")
        time.sleep(1)
        click_image(assets.BTN_AUTO, threshold=0.5)

        if fast_refresh:
            # Mode cepat: tidak nunggu tombol attack hilang (skip animasi skill yang lama)
            time.sleep(random.uniform(FAST_REFRESH_MIN, FAST_REFRESH_MAX))
        else:
            if _wait_attack_resolved():
                return True  # battle selesai saat nunggu
            time.sleep(1)

        log("🔙 Klik tombol back")
        click_back(threshold=0.5)

        # lanjut loop sampai result muncul
        time.sleep(1)


def _wait_attack_resolved():
    """
    Tunggu tombol attack hilang (aksi auto sudah jalan).
    Return True kalau battle berakhir di tengah jalan (bookmark sudah diklik),
    False kalau tombol attack hilang / timeout (caller lanjut klik back).
    """
    start_time = time.time()
    while True:
        screen = screenshot()
        time.sleep(0.3)

        if not match_template(screen, assets.BTN_ATTACK, threshold=0.4, preprocess=True):
            log("✅ Tombol attack hilang, battle action selesai")
            return False

        for sign in assets.BATTLE_END_SIGNS:
            if match_template(screen, sign, threshold=0.5, preprocess=True):
                log("⚠️ Battle End terdeteksi → klik bookmark dan keluar")
                click_bookmark()
                return True

        if time.time() - start_time > ATTACK_WAIT_TIMEOUT:
            log("⏰ Timeout 1 menit, tombol attack masih ada → langsung klik back")
            click_back(threshold=0.5)
            return False

        time.sleep(0.3)
