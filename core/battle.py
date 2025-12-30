# core/battle.py

import time
from utils.screenshot import *
from utils.config import raid_intro, setup
from core.button import button_reload

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

    setup_battle = setup.split(",")[0].strip().lower()

    # step 1: tunggu 1 detik sebelum mulai
    time.sleep(0.5)
    if raid_intro:
        button_reload()

    if setup_battle == "manual":
        manual()

    if setup_battle == "fa":
        fa()


def fa():
    fail_count = 0
    while True:
        screen = screenshot()

        # cek result screen
        if (match_template(screen, "assets/page/img_result_battle.png", threshold=0.7, preprocess=True) or
                match_template(screen, "assets/page/img_result_battle_2.png", threshold=0.7, preprocess=True)):
            print("✅ Battle selesai, result screen muncul")
            click_image_fullscreen("assets/button/bookmark.png", threshold=0.7)
            return True

        # cek tombol auto
        coords_auto = match_template(screen, "assets/button/auto.png", threshold=0.5, return_coords=True,
                                     preprocess=True)
        if not coords_auto:
            fail_count += 1
            print(f"⚠️ Tombol auto tidak ditemukan ({fail_count}/10)")
            time.sleep(1)

            if (match_template(screen, "assets/page/img_result_battle.png", threshold=0.6, preprocess=True) or
                    match_template(screen, "assets/page/img_result_battle_2.png", threshold=0.6, preprocess=True)):
                print("✅ Battle selesai, result screen muncul")
                click_image_fullscreen("assets/button/bookmark.png", threshold=0.7)
                return True

            if match_template(screen, "assets/button/dead.png", threshold=0.5, preprocess=True):
                print("⚠️ Party wipe")
                click_image_fullscreen("assets/button/bookmark.png", threshold=0.7)
                return True

            if fail_count >= 10:
                print("❌ Auto gagal ditemukan 10x, klik bookmark lalu keluar")
                click_image_fullscreen("assets/button/bookmark.png", threshold=0.7)
                return True

            continue

        # reset fail counter kalau ketemu auto
        fail_count = 0
        cx, cy, score = coords_auto
        print("✅ Tombol auto ditemukan → klik sekali")
        time.sleep(1)
        click_image_fullscreen("assets/button/auto.png", threshold=0.5)

        # tunggu sampai tombol attack hilang
        start_time = time.time()  # mulai hitung waktu
        while True:
            screen = screenshot()
            time.sleep(0.3)

            # cek kalau tombol attack masih ada
            if not match_template(screen, "assets/button/attack.png", threshold=0.4, preprocess=True):
                print("✅ Tombol attack hilang, battle action selesai")
                break

            # cek kalau battle end muncul
            if match_template(screen, "assets/button/battle_end.png", threshold=0.5, preprocess=True):
                print("⚠️ Battle End terdeteksi → klik bookmark dan keluar")
                click_image_fullscreen("assets/button/bookmark.png", threshold=0.7)
                return True
            if match_template(screen, "assets/button/battle_end_time.png", threshold=0.5, preprocess=True):
                print("⚠️ Battle End terdeteksi → klik bookmark dan keluar")
                click_image_fullscreen("assets/button/bookmark.png", threshold=0.7)
                return True
            if match_template(screen, "assets/button/dead.png", threshold=0.5, preprocess=True):
                print("⚠️ Battle End terdeteksi → klik bookmark dan keluar")
                click_image_fullscreen("assets/button/bookmark.png", threshold=0.7)
                return True

            if match_template(screen, "assets/page/party_wipe.png", threshold=0.5, preprocess=True):
                print("⚠️ Battle End terdeteksi → klik bookmark dan keluar")
                click_image_fullscreen("assets/button/bookmark.png", threshold=0.7)
                return True

            # cek kalau sudah lebih dari 60 detik tapi tombol attack masih ada
            if time.time() - start_time > 60:
                print("⏰ Timeout 1 menit, tombol attack masih ada → langsung klik back")
                click_image_fullscreen("assets/button/back.png", threshold=0.5)
                break

            time.sleep(0.3)

        # tunggu dikit biar aman sebelum klik back
        time.sleep(1)
        print("🔙 Klik tombol back")
        click_image_fullscreen("assets/button/back.png", threshold=0.5)


        # loop lanjut lagi, sampai result muncul
        time.sleep(1)

def manual():
    """
    Jalankan flow dari manual.json step by step.
    Kalau semua selesai → klik bookmark, return True.
    """

    global last_character_coords, last_character_position

    with open("manual.json", "r", encoding="utf-8") as f:
        flow = json.load(f)

    refresh = flow.get("refresh", False)

    # 🔎 Cek result battle sebelum mulai loop
    screen = screenshot()
    if (match_template(screen, "assets/page/img_result_battle.png", threshold=0.4, preprocess=True) or
        match_template(screen, "assets/page/img_result_battle_2.png", threshold=0.4, preprocess=True) or
        match_template(screen, "assets/page/exp_gained.png", threshold=0.4, preprocess=True)):
        print("✅ Battle selesai, result screen muncul")
        click_image_fullscreen("assets/button/bookmark.png", threshold=0.7)
        return True

    for i, step in enumerate(flow["steps"], start=1):
        action = step.get("action")
        target = step.get("target")
        skill_index = step.get("skill_index")

        print(f"🔄 Step {i}: {action}")

        # 🔎 cek result battle di awal step
        screen = screenshot()
        if (match_template(screen, "assets/page/img_result_battle.png", threshold=0.4, preprocess=True) or
            match_template(screen, "assets/page/img_result_battle_2.png", threshold=0.4, preprocess=True)):
            print("✅ Battle selesai, result screen muncul (awal step)")
            click_image_fullscreen("assets/button/bookmark.png", threshold=0.7)
            return True

        # cek tombol auto (skip untuk skill & summon)
        if action not in ["use_skill", "use_summon"]:
            if not wait_for_auto_button(timeout=20, debug=False):
                continue
            time.sleep(1)

        # eksekusi action
        if action == "select_character":
            coords = click_image_fullscreen_with_coords(
                f"assets/party/{target}.png", debug=False
            )
            if coords:
                last_character_coords = coords
                last_character_position = target
            else:
                print("[DEBUG] Karakter tidak ketemu → skip")

        elif action == "use_skill":
            if last_character_coords and last_character_position:
                click_skill_relative(
                    last_character_coords[0],
                    last_character_coords[1],
                    skill_index,
                    last_character_position,
                    debug=False,
                )
                if refresh:
                    time.sleep(0.5)
                    click_back_button(debug=False)
                print("✅ Skill berhasil ditekan")
            else:
                print("[DEBUG] Belum ada karakter yang dipilih → gak bisa klik skill")

        elif action == "select_summon":
            click_summon_button(debug=False)

        elif action == "quick_summon":
            click_quick_summon_button(debug=False)
            print("✅ Quick Summon berhasil")
            if refresh:
                time.sleep(0.5)
                click_back_button(debug=False)

        elif action == "auto":
            click_auto_button(debug=False)
            print("✅ Auto berhasil")
            if refresh:
                time.sleep(0.5)
                click_back_button(debug=False)

        elif action == "use_summon":
            summon_index = step.get("summon_index", 1)
            click_summon_index(summon_index, debug=False)
            time.sleep(0.5)
            click_ok_button()
            print("✅ Summon berhasil")
            if refresh:
                time.sleep(0.5)
                click_back_button(debug=False)

        elif action == "attack":
            click_image_fullscreen("assets/button/attack.png", debug=False)
            print("✅ Attack berhasil")
            if refresh:
                time.sleep(2)
                click_back_button(debug=False)

        # 🔎 cek result battle setelah action
        screen = screenshot()
        if (match_template(screen, "assets/page/img_result_battle.png", threshold=0.5, preprocess=True) or
            match_template(screen, "assets/page/img_result_battle_2.png", threshold=0.5, preprocess=True) or
            match_template(screen, "assets/page/exp_gained.png", threshold=0.5, preprocess=True)):
            print("✅ Battle selesai, result screen muncul")
            click_image_fullscreen("assets/button/bookmark.png", threshold=0.7)
            return True

        # delay antar step biar stabil
        time.sleep(1)

    # ✅ setelah semua step selesai, klik bookmark dan keluar
    print("✅ Semua step manual selesai → kembali ke main flow")
    click_image_fullscreen("assets/button/bookmark.png", threshold=0.7)
    return True
