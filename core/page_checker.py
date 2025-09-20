#page_checker.py
import time
from utils.screenshot import screenshot, match_template, click_image_fullscreen

def check_backup_request(image_path="assets/page/backup_requests.png"):
    """Loop cek halaman backup raid sampai benar."""
    while True:
        screen = screenshot()
        if match_template(screen, image_path, preprocess=False):
            print("✅ Sudah di halaman backup")
            return True
        else:
            print("❌ Harus ada di halaman backup raid")
            time.sleep(2)

def check_select_summon(image_path="assets/button/drop_items.png"):
    """cek halaman backup raid sampai benar."""
    while True:
        screen = screenshot()
        if match_template(screen, image_path, preprocess=False):
            print("✅ Sudah di halaman select summon")
            return True
        else:
            print("❌ Tidak berada di halaman select summon, balik bookmark...")
            click_image_fullscreen("assets/button/bookmark.png", threshold=0.7)
            time.sleep(2)
            return False
