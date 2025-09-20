import time
from utils.screenshot import *

def button_refresh():
    """
    Mengecek tombol reload. Klik jika ditemukan.
    Return True jika diklik, False jika tidak ditemukan.
    """
    screen = screenshot()
    button = "assets/button/refresh.png"
    if match_template(screen, button, threshold=0.4, preprocess=True):
        print("🔄 Tombol reload ditemukan, klik untuk refresh layar...")
        click_image_fullscreen(button, threshold=0.4)
        time.sleep(1)
        return False
    return False

def button_reload():
    """
    Mengecek tombol reload. Klik jika ditemukan.
    Return True jika diklik, False jika tidak ditemukan.
    """
    screen = screenshot()
    button = "assets/button/reload.png"
    if match_template(screen, button, threshold=0.4, preprocess=True):
        print("🔄 Tombol reload ditemukan, klik untuk refresh layar...")
        click_image_fullscreen(button, threshold=0.4)
        time.sleep(2)
        return True
    return False

def button_bookmark():
    """
    Mengecek tombol reload. Klik jika ditemukan.
    Return True jika diklik, False jika tidak ditemukan.
    """
    screen = screenshot()
    button = "assets/button/bookmark.png"
    if match_template(screen, button, threshold=0.4, preprocess=True):
        print("🔄 Tombol reload ditemukan, klik untuk refresh layar...")
        click_image_fullscreen(button, threshold=0.4)
        time.sleep(2)
        return True
    return False

