#utils/screenshot.py
import cv2
import numpy as np
import pyautogui
import os
import time
import json

def screenshot():
    """Ambil screenshot layar penuh (return numpy array BGR)."""
    img = pyautogui.screenshot()
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


def match_template(screen, template_path, threshold=0.7, return_coords=False,
                   preprocess=True, reject_dark=True, debug=False):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Template {template_path} tidak ditemukan.")

    gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    if preprocess:
        gray_screen = cv2.equalizeHist(gray_screen)
        template = cv2.equalizeHist(template)

        gray_screen = cv2.GaussianBlur(gray_screen, (3, 3), 0)
        template = cv2.GaussianBlur(template, (3, 3), 0)

        screen_bin = cv2.adaptiveThreshold(
            gray_screen, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        template_bin = cv2.adaptiveThreshold(
            template, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY, 11, 2
        )

        screen_proc = screen_bin
        template_proc = template_bin
    else:
        screen_proc = gray_screen
        template_proc = template

    res = cv2.matchTemplate(screen_proc, template_proc, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    # if debug:
        # print(f"[DEBUG] {os.path.basename(template_path)} score={max_val:.3f} (threshold={threshold})")

    if max_val >= threshold:
        h, w = template.shape
        cx = max_loc[0] + w // 2
        cy = max_loc[1] + h // 2

        # if reject_dark:
        #     is_dark, avg_brightness = is_dark_region(screen, (cx, cy), return_brightness=True)
        #     if debug:
        #         print(f"[DEBUG] brightness={avg_brightness:.1f} @ {template_path}")
        #     if is_dark:
        #         if debug:
        #             print(f"[DEBUG] {os.path.basename(template_path)} REJECT karena dark region")
        #         return False

        if return_coords:
            return (cx, cy, max_val)
        return True

    return False


def click_image(image_path, threshold=0.7, move_duration=0.1, debug=False):
    screen = screenshot()
    gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Template {image_path} tidak ditemukan.")

    # Cari di seluruh layar, bukan hanya ROI kiri
    res = cv2.matchTemplate(gray_screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if debug:
        print(f"[DEBUG] click_image {os.path.basename(image_path)} score={max_val:.3f}")

    if max_val < threshold:
        return False

    th, tw = template.shape[:2]
    cx, cy = max_loc[0] + tw // 2, max_loc[1] + th // 2

    pyautogui.moveTo(cx, cy, duration=move_duration)
    pyautogui.click()
    return True


def is_dark_region(screen, center, size=(100, 30), threshold=60, return_brightness=False):
    """
    Cek apakah region sekitar (x,y) lebih gelap dari threshold.
    Return bool (dan brightness kalau return_brightness=True).
    """
    x, y = center
    w, h = size
    roi = screen[max(0, y-h//2):y+h//2, max(0, x-w//2):x+w//2]

    if roi.size == 0:
        return (False, 999) if return_brightness else False

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray)

    if return_brightness:
        return avg_brightness < threshold, avg_brightness
    return avg_brightness < threshold


# 🔍 tool tambahan buat test semua template
def test_templates(templates, threshold=0.7, debug=True):
    screen = screenshot()
    for tpl in templates:
        match_template(screen, tpl, threshold=threshold, debug=debug)

def click_coords(cx, cy, move_duration=0.1):
    pyautogui.moveTo(cx, cy, duration=move_duration)
    pyautogui.click()

def click_image_fullscreen(image_path, threshold=0.7, move_duration=0.1, debug=False):
    screen = screenshot()
    gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Template {image_path} tidak ditemukan.")

    res = cv2.matchTemplate(gray_screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if debug:
        print(f"[DEBUG] click_image_fullscreen {os.path.basename(image_path)} score={max_val:.3f}")

    if max_val < threshold:
        return False

    th, tw = template.shape[:2]
    cx, cy = max_loc[0] + tw // 2, max_loc[1] + th // 2

    pyautogui.moveTo(cx, cy, duration=move_duration)
    pyautogui.click()
    return True

def click_skill_dynamic(skill_index, bar_template="assets/party/skill.png",
                        spacing=80, y_offset=20, threshold=0.7, debug=False):
    """
    Klik skill berdasarkan index, posisi bar dicari secara dinamis di layar penuh.
    Aman walau window dipindah/resize, asal skill bar kelihatan penuh.
    """
    screen = screenshot()
    bar_loc = match_template(screen, bar_template, threshold=threshold,
                             return_coords=True, debug=debug)
    if not bar_loc:
        if debug:
            print(f"[DEBUG] Skill bar {bar_template} tidak ditemukan di layar.")
        return False

    bx, by, score = bar_loc
    # Hitung posisi relatif skill ke-1,2,3,4
    cx = bx - (1.5 * spacing) + spacing * (skill_index - 1)
    cy = by + y_offset

    click_coords(cx, cy)
    time.sleep(0.5)

    if debug:
        print(f"[DEBUG] Dynamic klik skill {skill_index} di ({cx}, {cy}), score={score:.2f}")
    return True

def click_skill_relative(char_x, char_y, skill_index, position, debug=False):
    if isinstance(position, set):
        position = next(iter(position))

    if position == "1st":
        base_offset_x = 120
    elif position == "2nd":
        base_offset_x = 40
    elif position == "3rd":
        base_offset_x = -40
    elif position == "4th":
        base_offset_x = -120
    else:
        raise ValueError(f"Posisi '{position}' tidak valid!")

    base_offset_y = 95    # tetap sama
    skill_gap = 85        # jarak antar skill icon

    # Hitung posisi skill yang dimaksud
    x = char_x + base_offset_x + (skill_index - 1) * skill_gap
    y = char_y + base_offset_y

    if debug:
        print(f"[DEBUG] Klik skill {skill_index} relatif di ({x},{y})")

    pyautogui.click(x, y)
    return (x, y)

def click_image_fullscreen_with_coords(template_path, threshold=0.8, debug=False):
    result = find_image(template_path, threshold=threshold, debug=debug)
    if result:
        x, y = result
        pyautogui.click(x, y)
        if debug:
            print(f"[DEBUG] click_image_fullscreen_with_coords {template_path} di ({x},{y})")
        return (x, y)
    else:
        if debug:
            print(f"[DEBUG] Gagal find {template_path}")
        return None


def find_image(template_path, threshold=0.8, debug=False):
    """
    Cari template di screenshot layar penuh.
    Return (x,y) koordinat tengah gambar kalau ketemu, kalau tidak return None.
    """
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        if debug:
            print(f"[DEBUG] Template {template_path} tidak ditemukan (file missing).")
        return None

    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if debug:
        print(f"[DEBUG] match {template_path} score={max_val:.3f}")

    if max_val >= threshold:
        h, w = template.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        return (center_x, center_y)
    return None

def click_summon_button(debug=False):
    """Klik tombol summon di sidebar (assets/party/summon.png)."""
    return click_image_fullscreen("assets/party/summon.png", threshold=0.8, debug=debug)


def click_summon_index(summon_index, debug=False):
    """
    Klik summon berdasarkan urutan (1–6).
    summon_index: 1 = paling kiri, 6 = paling kanan
    """
    screen = screenshot()

    # Cari posisi popup summon -> patokannya tombol Heal (stabil di kiri bawah)
    heal_tpl = "assets/party/heal.png"
    loc = match_template(screen, heal_tpl, threshold=0.4, return_coords=True, debug=debug)
    if not loc:
        if debug:
            print("[DEBUG] Gagal menemukan anchor Heal button.")
        return False

    hx, hy, _ = loc

    # Offset relatif ke summon list
    base_offset_x = -50    # posisi summon pertama dari Heal
    base_offset_y = -110  # naik ke baris summon
    summon_gap = 75       # jarak antar summon

    x = hx + base_offset_x + (summon_index - 1) * summon_gap
    y = hy + base_offset_y

    if debug:
        print(f"[DEBUG] Klik summon {summon_index} di ({x},{y})")

    click_coords(x, y)
    return True

def click_quick_summon_button(debug=False):
    """Klik tombol summon di sidebar (assets/party/summon.png)."""
    return click_image_fullscreen("assets/button/quick_summon.png", threshold=0.8, debug=debug)

def click_auto_button(debug=False):
    """Klik tombol summon di sidebar (assets/party/summon.png)."""
    return click_image_fullscreen("assets/button/auto.png", threshold=0.8, debug=debug)

def click_back_button(debug=False):
    """Klik tombol summon di sidebar (assets/party/summon.png)."""
    return click_image_fullscreen("assets/button/reload.png", threshold=0.8, debug=debug)

def click_ok_button(debug=False):
    """Klik tombol summon di sidebar (assets/party/summon.png)."""
    return click_image_fullscreen("assets/button/ok.png", threshold=0.8, debug=debug)

def wait_for_auto_button(timeout=30, interval=0.5, debug=False):
    """
    Tunggu sampai tombol menu muncul di layar penuh.
    Return True kalau ketemu, False kalau timeout.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        found = find_image("assets/button/auto.png", threshold=0.8, debug=debug)
        if found:
            if debug:
                print("✅ Menu button muncul!")
            return True
        time.sleep(interval)

    if debug:
        print("❌ Menu button tidak ketemu setelah timeout")
    return False
