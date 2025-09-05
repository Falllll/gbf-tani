# from core.pop_up import battle_ended
from utils.image_utils import screenshot, match_template, click_image, click_coords, click_image_fullscreen
from core.page_checker import check_select_summon
from utils.config_utils import get_config, load_registry, get_raid_source_by_id
from core.pending_battle import handling_pending_battle
import time


def ensure_event_tab():
    """Pastikan kita sudah di tab Event pada backup request."""
    print("ℹ️ Event belum aktif, pindah tab...")

    if match_template(screenshot(), "assets/button/recent.png", threshold=0.7, preprocess=True):
        click_image("assets/button/recent.png", threshold=0.7)
        time.sleep(1)

    for _ in range(3):
        screen = screenshot()
        if match_template(screen, "assets/button/event_active.png", threshold=0.7, preprocess=True):
            print("✅ Sudah di tab Event (aktif)")
            return True

        if match_template(screen, "assets/button/event.png", threshold=0.7, preprocess=True):
            click_image("assets/button/event.png", threshold=0.7)
            time.sleep(1)
            print("✅ Berhasil pindah ke tab Event")
            return True

        time.sleep(0.5)

    print("❌ Gagal menemukan tombol Event (cek asset event.png / resolusi / scaling)")
    return False


def ensure_raid_tab():
    """Pastikan kita sudah di tab Finder pada backup request, lalu pilih raid sesuai config."""
    print("ℹ️ Raid belum aktif, pindah tab...")

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
            break

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
            break

        time.sleep(0.5)
    else:
        print("❌ Gagal menemukan tombol Finder")
        return False

    raid_id = get_config("raid_id")
    registry = load_registry()
    source = get_raid_source_by_id(raid_id, registry)

    if not source:
        print(f"❌ Raid ID {raid_id} tidak ditemukan di registry.json")
        return False

    print(f"🔍 Mulai cari raid")
    fail_count = 0
    while True:
        screen = screenshot()
        coords = match_template(
            screen,
            source,
            threshold=0.7,
            return_coords=True,
            preprocess=True
        )

        if coords:
            fail_count = 0
            cx, cy, score = coords
            print(f"✅ Raid ditemukan, memilih raid")
            time.sleep(0.5)
            click_coords(cx, cy)
            time.sleep(1)

            # 🔍 ambil screenshot ulang setelah klik (popup baru muncul di sini)
            popup_screen = screenshot()

            print(f"✅ Check Pop up")
            # --- cek popup umum ---
            popups = {
                "battle_ended": "assets/page/img_raid_battle_ended.png",
                "backup_3": "assets/page/img_3_backup.png",
                "battle_full": "assets/page/img_raid_battle_full.png"
            }

            for name, img in popups.items():
                if match_template(popup_screen, img, threshold=0.7, preprocess=True, reject_dark=False, debug=True):
                    print(f"⚠️ Popup terdeteksi: {name}")
                    # klik OK/bookmark
                    click_image_fullscreen("assets/page/bookmark.png", threshold=0.7)
                    return False  # ⬅️ balik ke loop utama

            # --- cek popup pending battle (beda penanganan) ---
            pending_battle_img = "assets/page/img_pending_battle.png"
            if match_template(popup_screen, pending_battle_img, threshold=0.4, preprocess=True, reject_dark=False,
                              debug=True):
                print("⚠️ Popup pending battle terdeteksi")
                handling_pending_battle()
                return False



            time.sleep(1)
            # ✅ kalau ga ada popup, lanjut ke summon
            if not check_select_summon():
                return False
            print(f"✅ Klik ok")
            click_image_fullscreen("assets/button/button_ok.png", threshold=0.7)

            # 🔍 setelah klik OK summon, cek apakah ada popup muncul lagi
            time.sleep(1.5)
            popup_screen = screenshot()

            print(f"✅ Check Pop up setelah summon OK")
            # --- cek popup umum ---
            popups = {
                "battle_ended": "assets/page/img_raid_battle_ended.png",
                "backup_3": "assets/page/img_3_backup.png",
                "battle_full": "assets/page/img_raid_battle_full.png"
            }

            print(f"✅ Check Pop up setelah summon OK")
            for name, img in popups.items():
                if match_template(popup_screen, img, threshold=0.7, preprocess=True, reject_dark=False, debug=True):
                    print(f"⚠️ Popup terdeteksi setelah summon OK: {name}")
                    click_image_fullscreen("assets/page/bookmark.png", threshold=0.7)
                    return False  # ⬅️ balik ke loop utama


            # --- cek popup pending battle (beda penanganan) ---
            pending_battle_img = "assets/page/img_pending_battle.png"
            if match_template(popup_screen, pending_battle_img, threshold=0.4, preprocess=True, reject_dark=False,
                              debug=True):
                print("⚠️ Popup pending battle terdeteksi setelah summon OK")
                handling_pending_battle()
                continue

            pending_battle_img = "assets/page/captcha.png"
            if match_template(popup_screen, pending_battle_img, threshold=0.5, preprocess=True, reject_dark=False,
                              debug=True):
                print("⚠️ CAPTCHA TERDETEKSI HENTIKAN PROGRAM!!!")
                exit()

            # ✅ kalau udah sampai sini berarti summon aman → keluar ke main.py
            return True
        else:
            # 🔄 coba klik tombol reload dulu
            reload_btn = "assets/button/reload.png"
            if match_template(screen, reload_btn, threshold=0.7, preprocess=True):
                print("🔄 Tombol reload ditemukan, klik untuk refresh layar...")
                click_image_fullscreen(reload_btn, threshold=0.7)
                time.sleep(2)
                continue  # skip increment fail_count, langsung ulangi loop

            # kalau reload gak ada → baru dianggap gagal
            fail_count += 1
            print(f"⚠️ Raid tidak dikenali di layar (score < threshold / asset beda), ulangi... ({fail_count}/10)")
            time.sleep(2)

            if fail_count >= 10:
                print("❌ Raid gagal terdeteksi 10x, klik bookmark lalu ulangi pencarian...")
                click_image_fullscreen("assets/page/bookmark.png", threshold=0.7)
                fail_count = 0  # reset counter
                continue