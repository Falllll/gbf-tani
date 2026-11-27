# gbf_tani/game/party.py
"""Klik karakter, skill, dan summon. Offset pixel dikalibrasi ke layout layar sekarang."""
import pyautogui

from gbf_tani import assets
from gbf_tani.vision.capture import screenshot
from gbf_tani.vision.matcher import match_template
from gbf_tani.vision.mouse import click_coords, click_image

# Offset X ikon skill pertama, relatif ke posisi karakter
SKILL_BASE_OFFSET_X = {
    "1st": 120,
    "2nd": 40,
    "3rd": -40,
    "4th": -120,
}
SKILL_BASE_OFFSET_Y = 95
SKILL_GAP = 85

# Offset summon, relatif ke tombol Heal (anchor stabil)
SUMMON_BASE_OFFSET_X = -50
SUMMON_BASE_OFFSET_Y = -110
SUMMON_GAP = 75


def click_skill_relative(char_x, char_y, skill_index, position, debug=False):
    """Klik skill ke-N (1–4) dari karakter di posisi '1st'..'4th'."""
    if isinstance(position, set):
        position = next(iter(position))

    if position not in SKILL_BASE_OFFSET_X:
        raise ValueError(f"Posisi '{position}' tidak valid!")

    x = char_x + SKILL_BASE_OFFSET_X[position] + (skill_index - 1) * SKILL_GAP
    y = char_y + SKILL_BASE_OFFSET_Y

    if debug:
        print(f"[DEBUG] Klik skill {skill_index} relatif di ({x},{y})")

    pyautogui.click(x, y)
    return (x, y)


def click_summon_button(debug=False):
    """Klik tombol summon di sidebar."""
    return click_image(assets.PARTY_SUMMON, threshold=0.8, debug=debug)


def click_summon_index(summon_index, debug=False):
    """Klik summon berdasarkan urutan (1 = paling kiri … 6 = paling kanan)."""
    loc = match_template(screenshot(), assets.PARTY_HEAL, threshold=0.4, return_coords=True)
    if not loc:
        if debug:
            print("[DEBUG] Gagal menemukan anchor Heal button.")
        return False

    hx, hy = loc.x, loc.y
    x = hx + SUMMON_BASE_OFFSET_X + (summon_index - 1) * SUMMON_GAP
    y = hy + SUMMON_BASE_OFFSET_Y

    if debug:
        print(f"[DEBUG] Klik summon {summon_index} di ({x},{y})")

    click_coords(x, y)
    return True
