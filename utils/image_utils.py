import cv2
import numpy as np
import pyautogui
import os

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

    if debug:
        print(f"[DEBUG] {os.path.basename(template_path)} score={max_val:.3f} (threshold={threshold})")

    if max_val >= threshold:
        h, w = template.shape
        cx = max_loc[0] + w // 2
        cy = max_loc[1] + h // 2

        if reject_dark:
            is_dark, avg_brightness = is_dark_region(screen, (cx, cy), return_brightness=True)
            if debug:
                print(f"[DEBUG] brightness={avg_brightness:.1f} @ {template_path}")
            if is_dark:
                if debug:
                    print(f"[DEBUG] {os.path.basename(template_path)} REJECT karena dark region")
                return False

        if return_coords:
            return (cx, cy, max_val)
        return True

    return False


def click_image(image_path, threshold=0.7, move_duration=0.1, debug=False):
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

    roi = cv2.normalize(roi, None, 0, 255, cv2.NORM_MINMAX)
    template = cv2.normalize(template, None, 0, 255, cv2.NORM_MINMAX)

    res = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if debug:
        print(f"[DEBUG] click_image {os.path.basename(image_path)} score={max_val:.3f}")

    if max_val < threshold:
        return False

    th, tw = template.shape[:2]
    rx, ry = max_loc
    cx, cy = rx + tw // 2, ry + th // 2

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
