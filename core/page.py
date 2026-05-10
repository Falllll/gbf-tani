# core/page.py
import time
from utils.variable import *
from utils.screenshot import *
from core.finder import select_raid
from core.battle import fa
from core.popup import check_captcha
from core.button import button_reload

def check_tab(mode: str) -> bool:
    if mode == "finder":
        raid_page()
    if mode == "solo":
        attempt = 0
        while True:
            screen = screenshot()

            if match_template(screen, page_backup_solo, preprocess=False):
                print("✅ Sudah di halaman solo")
                click_ok_button()
                time.sleep(0.5)

                screen = screenshot()
                if check_captcha(screen, debug=True):
                    print("⚠️ CAPTCHA terdeteksi, hentikan program.")
                    exit()

                if wait_for_auto_button(timeout=30, interval=0.5, debug=False):
                    fa()
                else:
                    print("⚠️ Tombol auto tidak muncul setelah klik OK")
                return True
            if match_template(screen, page_senbok, preprocess=False):
                print("✅ Sudah di halaman senbok")
                return True
            if match_template(screen, "assets/page/in_battle.png", preprocess=False):
                print("✅ Sudah di halaman battle, jalankan auto")
                fa()
                return True
            attempt += 1
            print(f"❌ Harus ada di halaman solo (percobaan {attempt})")
            if attempt >= 10:
                print("🔄 30x gagal, klik bookmark untuk reset")
                button_reload()
                time.sleep(1)
                click_image_fullscreen("assets/button/bookmark.png", threshold=0.7)
                attempt = 0
            time.sleep(2)
    if mode == "event":
        while True:
            screen = screenshot()

            if match_template(screen, page_backup_requests, preprocess=False):
                print("✅ Sudah di halaman backup")
                return True
            else:
                print("❌ Harus ada di halaman backup raid")
                button_reload()
                time.sleep(2)
                click_image_fullscreen("assets/button/bookmark.png", threshold=0.7)
    return False

def raid_page():
    attempt = 0  # hitungan percobaan
    while True:
        screen = screenshot()
        if match_template(screen, page_backup_requests, preprocess=False):
            print("✅ Sudah di halaman backup")
            print("ℹ️ Cek apakah sudah di tab finder jika belum, pindah tab...")

            for _ in range(3):
                screen = screenshot()
                coords_active = match_template(
                    screen,
                    "assets/button/finder_active.png",
                    threshold=0.4,
                    return_coords=True,
                    preprocess=True
                )
                if coords_active:
                    print("✅ Sudah di tab Finder (aktif)")
                    return select_raid()

                coords_normal = match_template(
                    screen,
                    "assets/button/finder.png",
                    threshold=0.4,
                    return_coords=True,
                    preprocess=True
                )
                if coords_normal:
                    click_image("assets/button/finder.png", threshold=0.4)
                    time.sleep(1)
                    print("✅ Berhasil pindah ke tab Finder")
                    return select_raid()

                time.sleep(0.5)

            else:
                print("❌ Gagal menemukan tombol Finder")
                attempt += 1
                print(f"⚠️ Percobaan gagal ke-{attempt}/30")

                if attempt >= 10:
                    print("🔄 30x gagal, klik bookmark untuk reset")
                    button_reload()
                    time.sleep(1)
                    click_image_fullscreen("assets/button/bookmark.png", threshold=0.7)
                    attempt = 0  # reset count

        else:
            print("❌ Harus ada di halaman backup raid")
            time.sleep(2)
            attempt += 1
            print(f"⚠️ Percobaan gagal ke-{attempt}/10")

            if attempt >= 10:
                print("🔄 30x gagal, klik bookmark untuk reset")
                button_reload()
                time.sleep(1)
                click_image_fullscreen("assets/button/bookmark.png", threshold=0.7)
                attempt = 0  # reset count
