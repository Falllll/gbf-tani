from utils.screenshot import screenshot, match_template, click_coords, click_image_fullscreen
from utils.config import raid_id, raid_source
import time

def handling_pending_battle(debug=False):
    print("⚠️ Handling pending battle...")

    # Klik OK popup
    click_image_fullscreen("assets/button/button_ok.png", threshold=0.7)
    time.sleep(1)

    while True:
        screen = screenshot()
        coords = match_template(
            screen,
            raid_source,
            threshold=0.4,
            return_coords=True,
            preprocess=True
        )

        if not coords:
            print("✅ Tidak ada raid pending lagi, keluar dari handling_pending_battle")
            click_image_fullscreen("assets/button/bookmark.png", threshold=0.7)
            return True

        cx, cy, score = coords
        print(f"➡️ Klik raid pending (score={score:.3f})")
        click_coords(cx, cy)
        time.sleep(1)

        # Tunggu result battle
        found_result = False
        for _ in range(10):
            result_screen = screenshot()
            if match_template(result_screen, "assets/page/img_result_battle.png", threshold=0.6, preprocess=True, reject_dark=False) \
               or match_template(result_screen, "assets/page/img_result_battle_2.png", threshold=0.6, preprocess=True, reject_dark=False):
                print("✅ Result battle terdeteksi, klik Back")
                click_image_fullscreen("assets/button/back.png", threshold=0.7)
                time.sleep(2)
                found_result = True
                break
            time.sleep(1)

        if not found_result:
            print("⚠️ Result battle tidak muncul setelah 10 detik, klik bookmark untuk reset")
            click_image_fullscreen("assets/button/bookmark.png", threshold=0.7)
            time.sleep(1)
