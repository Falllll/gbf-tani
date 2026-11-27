# gbf_tani/vision/mouse.py
import os
import random
import time

import pyautogui

from gbf_tani import context
from gbf_tani.vision.matcher import find_raw, find_image_box
from gbf_tani.log import log

# Jarak aman dari pinggir gambar, dalam persen ukuran gambar per sisi.
# 0.25 → klik selalu jatuh di 50% area tengah (25% kiri/kanan/atas/bawah tidak pernah diklik).
CLICK_MARGIN_RATIO = 0.25
# Jarak aman minimum dalam pixel, untuk gambar kecil.
CLICK_MARGIN_MIN_PX = 3

# Jeda acak (detik) setelah gambar ketemu, sebelum mouse gerak & klik.
CLICK_DELAY_MIN = 0.2
CLICK_DELAY_MAX = 0.7


def wait_before_click():
    """Tunggu acak CLICK_DELAY_MIN–CLICK_DELAY_MAX detik."""
    time.sleep(random.uniform(CLICK_DELAY_MIN, CLICK_DELAY_MAX))


def random_point_in_box(box, margin_ratio=CLICK_MARGIN_RATIO, min_margin=CLICK_MARGIN_MIN_PX):
    """
    Titik acak di dalam box (left, top, width, height), menjauhi pinggir.
    Kalau gambar terlalu kecil untuk margin-nya, sumbu itu pakai titik tengah.
    """
    left, top, width, height = box
    return (
        _random_axis(left, width, margin_ratio, min_margin),
        _random_axis(top, height, margin_ratio, min_margin),
    )


def _random_axis(start, size, margin_ratio, min_margin):
    margin = max(min_margin, int(size * margin_ratio))
    low = start + margin
    high = start + size - 1 - margin
    if high < low:
        return start + size // 2
    return random.randint(low, high)


def click_coords(cx, cy, move_duration=0.1):
    """Gerakkan mouse ke (cx, cy) lalu klik. Koordinat relatif jendela akun (layar penuh di mode 1 akun)."""
    if context.region() is None:
        # --- 1 akun (perilaku lama, tidak diubah) ---
        pyautogui.moveTo(cx, cy, duration=move_duration)
        pyautogui.click()
    else:
        # --- multi akun: geser ke koordinat layar, antre pakai mouse ---
        x, y = context.to_screen(cx, cy)
        with context.INPUT_LOCK:
            pyautogui.moveTo(x, y, duration=move_duration)
            pyautogui.click()


def click_instant(cx, cy):
    """Klik langsung di (cx, cy) tanpa animasi gerak. Koordinat relatif jendela akun."""
    if context.region() is None:
        # --- 1 akun (perilaku lama, tidak diubah) ---
        pyautogui.click(cx, cy)
    else:
        # --- multi akun ---
        x, y = context.to_screen(cx, cy)
        with context.INPUT_LOCK:
            pyautogui.click(x, y)


def click_box(box, move_duration=0.1):
    """Gambar sudah ketemu → jeda acak → klik titik acak di area gambar."""
    wait_before_click()
    click_coords(*random_point_in_box(box), move_duration=move_duration)


def click_image(image_path, threshold=0.7, move_duration=0.1, debug=False):
    """
    Screenshot baru, cari template (grayscale mentah) di layar penuh,
    klik titik acak di area gambar. Return True kalau diklik, False kalau tidak ketemu.
    """
    box, score = find_raw(image_path, threshold)

    if debug:
        log(f"[DEBUG] click_image_fullscreen {os.path.basename(image_path)} score={score:.3f}")

    if box is None:
        return False

    click_box(box, move_duration=move_duration)
    return True


def click_image_with_coords(template_path, threshold=0.8, debug=False):
    """
    Cari template (warna) lalu klik titik acak di area gambar.
    Return (x, y) titik TENGAH gambar (bukan titik yang diklik) — dipakai sebagai
    patokan offset skill, jadi harus stabil. None kalau tidak ketemu.
    """
    box = find_image_box(template_path, threshold=threshold, debug=debug)
    if not box:
        if debug:
            log(f"[DEBUG] Gagal find {template_path}")
        return None

    left, top, w, h = box
    center = (left + w // 2, top + h // 2)
    wait_before_click()
    click_instant(*random_point_in_box(box))
    if debug:
        log(f"[DEBUG] click_image_fullscreen_with_coords {template_path} di {center}")
    return center
