#popup.py
import time
from utils.image_utils import screenshot, match_template

# def battle_ended(image_path="assets/page/img_raid_battle_ended.png"):


def check_select_summon(image_path="assets/button/drop_items.png"):
    """cek halaman backup raid sampai benar."""
    while True:
        screen = screenshot()
        if match_template(screen, image_path, preprocess=False):
            print("✅ Sudah di halaman select summon")
            return True
        else:
            print("❌ Tidak berada di halaman select summon")
            time.sleep(2)