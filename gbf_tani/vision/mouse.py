# gbf_tani/vision/mouse.py
import os

import pyautogui

from gbf_tani.vision.matcher import find_raw, find_image


def click_coords(cx, cy, move_duration=0.1):
    pyautogui.moveTo(cx, cy, duration=move_duration)
    pyautogui.click()


def click_image(image_path, threshold=0.7, move_duration=0.1, debug=False):
    """
    Screenshot baru, cari template (grayscale mentah) di layar penuh, klik tengahnya.
    Return True kalau diklik, False kalau tidak ketemu.
    """
    center, score = find_raw(image_path, threshold)

    if debug:
        print(f"[DEBUG] click_image_fullscreen {os.path.basename(image_path)} score={score:.3f}")

    if center is None:
        return False

    click_coords(*center, move_duration=move_duration)
    return True


def click_image_with_coords(template_path, threshold=0.8, debug=False):
    """Cari template (warna) lalu klik. Return (x, y) kalau diklik, None kalau tidak."""
    result = find_image(template_path, threshold=threshold, debug=debug)
    if not result:
        if debug:
            print(f"[DEBUG] Gagal find {template_path}")
        return None

    x, y = result
    pyautogui.click(x, y)
    if debug:
        print(f"[DEBUG] click_image_fullscreen_with_coords {template_path} di ({x},{y})")
    return (x, y)
