import time
from utils.image_utils import screenshot, match_template

def check_backup_request(image_path="assets/page/backup_requests.png"):
    """Loop cek halaman backup raid sampai benar."""
    while True:
        screen = screenshot()
        if match_template(screen, image_path):
            print("✅ Sudah di halaman backup")
            return True
        else:
            print("❌ Harus ada di halaman backup raid")
            time.sleep(2)
