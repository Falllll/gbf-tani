# core/battle.py

import time
from utils.image_utils import screenshot, match_template, click_image_fullscreen

def handle_battle():
    """
    Handle battle flow:
    1. Tunggu 1 detik, cek tombol auto.
    2. Kalau ga ada auto sampai 10x → klik bookmark, return True.
    3. Kalau ada auto → klik sekali, tunggu tombol attack hilang.
    4. Setelah attack hilang → tunggu 1 detik, klik back.
    5. Ulangi sampai result battle muncul.
    6. Kalau result battle muncul → klik bookmark, return True.
    """

    # step 1: tunggu 1 detik sebelum mulai
    time.sleep(1)

    fail_count = 0
    while True:
        screen = screenshot()

        # cek result screen
        if (match_template(screen, "assets/page/img_result_battle.png", threshold=0.7, preprocess=True) or
            match_template(screen, "assets/page/img_result_battle_2.png", threshold=0.7, preprocess=True)):
            print("✅ Battle selesai, result screen muncul")
            click_image_fullscreen("assets/page/bookmark.png", threshold=0.7)
            return True

        # cek tombol auto
        coords_auto = match_template(screen, "assets/button/auto.png", threshold=0.5, return_coords=True, preprocess=True)
        if not coords_auto:
            fail_count += 1
            print(f"⚠️ Tombol auto tidak ditemukan ({fail_count}/10)")
            time.sleep(1)

            if fail_count >= 10:
                print("❌ Auto gagal ditemukan 10x, klik bookmark lalu keluar")
                click_image_fullscreen("assets/page/bookmark.png", threshold=0.7)
                return True

            continue

        # reset fail counter kalau ketemu auto
        fail_count = 0
        cx, cy, score = coords_auto
        print("✅ Tombol auto ditemukan → klik sekali")
        time.sleep(1)
        click_image_fullscreen("assets/button/auto.png", threshold=0.5)

        # tunggu sampai tombol attack hilang
        while True:
            screen = screenshot()
            if not match_template(screen, "assets/button/attack.png", threshold=0.5, preprocess=True):
                print("✅ Tombol attack hilang, battle action selesai")
                break
            time.sleep(0.5)

        # tunggu dikit biar aman sebelum klik back
        time.sleep(1)
        print("🔙 Klik tombol back")
        click_image_fullscreen("assets/button/back.png", threshold=0.5)

        # loop lanjut lagi, sampai result muncul
        time.sleep(1)
