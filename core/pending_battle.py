import time
from utils.image_utils import *
from utils.config_utils import get_config, load_registry, get_raid_source_by_id

def handling_pending_battle():
    print("⚠️ Handling pending battle...")

    # klik OK popup
    click_image_fullscreen("assets/button/button_ok.png", threshold=0.7)
    time.sleep(1)

    raid_id = get_config("raid_id")
    registry = load_registry()
    source = get_raid_source_by_id(raid_id, registry)

    while True:
        screen = screenshot()
        raids = match_template(
            screen,
            source,
            threshold=0.4,
            return_coords=True,
            preprocess=True
        )

        if not raids:
            print("✅ Tidak ada raid pending lagi, keluar dari handling_pending_battle")
            click_image_fullscreen("assets/page/bookmark.png", threshold=0.7)
            return True

        # klik raid pending
        cx, cy, score = raids
        print(f"➡️ Klik raid pending (score={score:.3f})")
        click_coords(cx, cy)
        time.sleep(1)

        # tunggu result battle muncul (max 10x loop)
        found_result = False
        for i in range(10):
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
            click_image_fullscreen("assets/page/bookmark.png", threshold=0.7)
            time.sleep(1)
