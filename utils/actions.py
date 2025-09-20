import time
import cv2
import os
from utils.screenshot import screenshot, match_template, click_coords

def _click_image(template_path, threshold=0.7, debug=False, delay=0.5):
    if not os.path.exists(template_path):
        if debug:
            print(f"[ERROR] Template tidak ditemukan: {template_path}")
        return None
    screen = screenshot()
    coords = match_template(screen, template_path, threshold=threshold, return_coords=True, debug=debug)
    if coords:
        cx, cy, score = coords
        if debug:
            print(f"[DEBUG] Klik {os.path.basename(template_path)} @({cx},{cy}) score={score:.3f}")
        click_coords(cx, cy)
        time.sleep(delay)
        return (cx, cy)
    else:
        if debug:
            print(f"[WARN] Tidak menemukan {template_path}")
        return None

# === Aksi Karakter ===
def select_character(char_template, debug=False):
    return _click_image(char_template, debug=debug)

def open_skill_bar(skill_bar_template, debug=False):
    """Temukan posisi skill bar, return koordinat tengah bar."""
    return _click_image(skill_bar_template, debug=debug)

def use_skill(skill_bar_coords, skill_index=1, spacing=80, debug=False):
    """
    Klik skill berdasarkan koordinat relatif:
    - skill_bar_coords: koordinat bar skill (hasil open_skill_bar)
    - skill_index: nomor skill (1-4)
    - spacing: jarak horizontal antar skill icon
    """
    if not skill_bar_coords:
        if debug:
            print("[ERROR] Skill bar tidak ditemukan")
        return False
    cx, cy = skill_bar_coords
    # Klik di bawah bar, bergeser horizontal per skill
    target_x = cx + (skill_index - 2.5) * spacing  # geser relatif: tengah bar = skill2/3
    target_y = cy + 50  # klik sedikit di bawah bar
    if debug:
        print(f"[DEBUG] Klik skill {skill_index} di ({int(target_x)}, {int(target_y)})")
    click_coords(int(target_x), int(target_y))
    time.sleep(0.5)
    return True

def attack(attack_btn_template, debug=False):
    return _click_image(attack_btn_template, debug=debug)

def quick_summon(summon_template, debug=False):
    return _click_image(summon_template, debug=debug)

def select_summon(summon_slot_template, debug=False):
    return _click_image(summon_slot_template, debug=debug)
