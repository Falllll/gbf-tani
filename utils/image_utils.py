import cv2
import numpy as np
import pyautogui

def screenshot():
    """Ambil screenshot layar penuh (return numpy array BGR)."""
    img = pyautogui.screenshot()
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


def match_template(screen, template_path, threshold=0.7, return_coords=False):
    """
    Cari template image di screenshot.
    Bisa deteksi meski tab Event aktif/nonaktif dengan fokus ke teks.
    return_coords = True → return (x, y, confidence)
    """

    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Template {template_path} tidak ditemukan.")

    gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    # --- Preprocessing: fokus huruf, buang background ---
    # ambil edge (huruf jadi putih, background mostly hilang)
    template_edge = cv2.Canny(template, 50, 150)
    screen_edge = cv2.Canny(gray_screen, 50, 150)

    # --- Matching ---
    res = cv2.matchTemplate(screen_edge, template_edge, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # print(f"[DEBUG] {template_path} confidence={max_val:.3f}")

    if max_val >= threshold:
        if return_coords:
            h, w = template.shape
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            return (center_x, center_y, max_val)
        return True
    return False

def click_image(image_path, threshold=0.7, move_duration=0.1):
    """
    Klik pada center image kalau ketemu.
    Bisa mengenali tombol dalam kondisi active/inactive dengan 1 template.
    Return True kalau berhasil klik, False kalau tidak ditemukan.
    """
    screen = screenshot()
    gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    h, w = gray_screen.shape
    roi = gray_screen[0:h//2, 0:w//3]

    template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Template {image_path} tidak ditemukan.")

    # Normalisasi biar lebih robust
    roi = cv2.normalize(roi, None, 0, 255, cv2.NORM_MINMAX)
    template = cv2.normalize(template, None, 0, 255, cv2.NORM_MINMAX)

    res = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if max_val < threshold:
        return False

    th, tw = template.shape[:2]
    rx, ry = max_loc
    cx, cy = rx + tw // 2, ry + th // 2

    pyautogui.moveTo(cx, cy, duration=move_duration)
    pyautogui.click()
    return True

def is_dark_region(screen, center, size=(100, 30), threshold=80):
    """
    Cek apakah region sekitar (x,y) lebih gelap dari threshold.
    Dipakai buat bedain tombol aktif (gelap) atau nonaktif (terang).
    """
    x, y = center
    w, h = size
    roi = screen[max(0, y-h//2):y+h//2, max(0, x-w//2):x+w//2]

    if roi.size == 0:
        return False

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray)
    # print(f"[DEBUG] Brightness={avg_brightness:.1f}")
    return avg_brightness < threshold