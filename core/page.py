# core/page.py
import time
from utils.variable import *
from utils.screenshot import *
from core.finder import select_raid

def check_tab(mode: str) -> bool:
    if mode == "finder":
        raid_page()
    if mode == "solo":
        while True:
            screen = screenshot()

            if match_template(screen, page_backup_solo, preprocess=False):
                print("✅ Sudah di halaman solo")
                return True
            if match_template(screen, page_senbok, preprocess=False):
                print("✅ Sudah di halaman senbok")
                return True
            else:
                print("❌ Harus ada di halaman solo")
                time.sleep(2)
    if mode == "event":
        while True:
            screen = screenshot()

            if match_template(screen, page_backup_requests, preprocess=False):
                print("✅ Sudah di halaman backup")
                return True
            else:
                print("❌ Harus ada di halaman backup raid")
                time.sleep(2)
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

                if attempt >= 30:
                    print("🔄 30x gagal, klik bookmark untuk reset")
                    click_image_fullscreen("assets/button/bookmark.png", threshold=0.7)
                    attempt = 0  # reset count

        else:
            print("❌ Harus ada di halaman backup raid")
            time.sleep(2)
            attempt += 1
            print(f"⚠️ Percobaan gagal ke-{attempt}/30")

            if attempt >= 30:
                print("🔄 30x gagal, klik bookmark untuk reset")
                click_image_fullscreen("assets/button/bookmark.png", threshold=0.7)
                attempt = 0  # reset count
