# gbf_tani/vision/matcher.py
from typing import NamedTuple

import cv2

from gbf_tani.vision.capture import screenshot
from gbf_tani.log import log


class Match(NamedTuple):
    """Hasil match: titik tengah, skor, dan kotak area template (left, top, width, height)."""
    x: int
    y: int
    score: float
    box: tuple


def _binarize(gray):
    """Equalize → blur → adaptive threshold. Dipakai ke layar & template."""
    gray = cv2.equalizeHist(gray)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    return cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY, 11, 2
    )


def match_template(screen, template_path, threshold=0.7, return_coords=False, preprocess=True):
    """
    Cari template di screen (BGR).
    Return:
        return_coords=False → True/False
        return_coords=True  → Match(x, y, score, box) atau False
    """
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Template {template_path} tidak ditemukan.")

    gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    if preprocess:
        screen_proc = _binarize(gray_screen)
        template_proc = _binarize(template)
    else:
        screen_proc = gray_screen
        template_proc = template

    res = cv2.matchTemplate(screen_proc, template_proc, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if max_val < threshold:
        return False

    if return_coords:
        h, w = template.shape
        cx = max_loc[0] + w // 2
        cy = max_loc[1] + h // 2
        return Match(cx, cy, max_val, (max_loc[0], max_loc[1], w, h))
    return True


def match_any(screen, template_paths, threshold=0.7, preprocess=True):
    """True kalau salah satu template ketemu. Dicek berurutan, berhenti di match pertama."""
    for path in template_paths:
        if match_template(screen, path, threshold=threshold, preprocess=preprocess):
            return True
    return False


def find_raw(template_path, threshold):
    """
    Screenshot baru + cocokkan grayscale mentah (tanpa preprocess).
    Return (box, score). box = (left, top, width, height), atau None kalau tidak lolos threshold.
    """
    screen = screenshot()
    gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Template {template_path} tidak ditemukan.")

    res = cv2.matchTemplate(gray_screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if max_val < threshold:
        return None, max_val

    th, tw = template.shape[:2]
    return (max_loc[0], max_loc[1], tw, th), max_val


def find_image(template_path, threshold=0.8, debug=False):
    """
    Cari template (warna) di screenshot layar penuh.
    Return (x, y) koordinat tengah kalau ketemu, None kalau tidak.
    """
    box = find_image_box(template_path, threshold=threshold, debug=debug)
    if box is None:
        return None
    left, top, w, h = box
    return (left + w // 2, top + h // 2)


def find_image_box(template_path, threshold=0.8, debug=False):
    """Sama seperti find_image, tapi return kotak (left, top, width, height)."""
    screen = screenshot()

    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        if debug:
            log(f"[DEBUG] Template {template_path} tidak ditemukan (file missing).")
        return None

    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if debug:
        log(f"[DEBUG] match {template_path} score={max_val:.3f}")

    if max_val >= threshold:
        h, w = template.shape[:2]
        return (max_loc[0], max_loc[1], w, h)
    return None
