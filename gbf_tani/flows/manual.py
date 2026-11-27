# gbf_tani/flows/manual.py
"""Mode manual: jalankan langkah-langkah dari manual.json satu per satu."""
import json
import time

from gbf_tani import assets
from gbf_tani.config import MANUAL_FILE
from gbf_tani.game.buttons import (
    click_auto_button,
    click_bookmark,
    click_ok_button,
    click_quick_summon_button,
    click_reload_button,
    wait_for_auto_button,
)
from gbf_tani.game.party import click_skill_relative, click_summon_button, click_summon_index
from gbf_tani.game.popups import is_battle_result
from gbf_tani.vision.capture import screenshot
from gbf_tani.vision.mouse import click_image, click_image_with_coords

# Aksi yang TIDAK perlu nunggu tombol auto dulu
NO_WAIT_ACTIONS = ("use_skill", "use_summon")

# Karakter terakhir yang dipilih (dipakai use_skill). Bertahan antar battle.
last_character_coords = None
last_character_position = None


def _refresh(refresh, delay=0.5):
    """Kalau manual.json minta refresh → tunggu lalu klik reload."""
    if refresh:
        time.sleep(delay)
        click_reload_button(debug=False)


# ---------------------------------------------------------------------------
# Handler per aksi: handler(step, refresh)
# ---------------------------------------------------------------------------

def _select_character(step, refresh):
    global last_character_coords, last_character_position
    target = step.get("target")
    coords = click_image_with_coords(assets.party_slot(target), debug=False)
    if coords:
        last_character_coords = coords
        last_character_position = target
    else:
        print("[DEBUG] Karakter tidak ketemu → skip")


def _use_skill(step, refresh):
    if not (last_character_coords and last_character_position):
        print("[DEBUG] Belum ada karakter yang dipilih → gak bisa klik skill")
        return

    click_skill_relative(
        last_character_coords[0],
        last_character_coords[1],
        step.get("skill_index"),
        last_character_position,
        debug=False,
    )
    _refresh(refresh)
    print("✅ Skill berhasil ditekan")


def _select_summon(step, refresh):
    click_summon_button(debug=False)


def _quick_summon(step, refresh):
    print("✅ Quick Summon dipilih")
    click_quick_summon_button(debug=False)
    print("✅ Quick Summon berhasil")
    _refresh(refresh)


def _auto(step, refresh):
    click_auto_button(debug=False)
    print("✅ Auto berhasil")
    _refresh(refresh)


def _use_summon(step, refresh):
    click_summon_index(step.get("summon_index", 1), debug=False)
    time.sleep(0.5)
    click_ok_button()
    print("✅ Summon berhasil")
    _refresh(refresh)


def _attack(step, refresh):
    click_image(assets.BTN_ATTACK, debug=False)
    print("✅ Attack berhasil")
    _refresh(refresh, delay=2)


ACTIONS = {
    "select_character": _select_character,
    "use_skill": _use_skill,
    "select_summon": _select_summon,
    "quick_summon": _quick_summon,
    "auto": _auto,
    "use_summon": _use_summon,
    "attack": _attack,
}


def _finish_if_result(with_exp, label="✅ Battle selesai, result screen muncul"):
    """Kalau layar result muncul → print, klik bookmark, return True."""
    if is_battle_result(screenshot(), threshold=0.6, with_exp=with_exp):
        print(label)
        click_bookmark()
        return True
    return False


def manual():
    """
    Jalankan flow dari manual.json step by step.
    Kalau result muncul atau semua step selesai → klik bookmark, return True.
    """
    with open(MANUAL_FILE, "r", encoding="utf-8") as f:
        flow = json.load(f)

    refresh = flow.get("refresh", False)

    if _finish_if_result(with_exp=True):
        return True

    for i, step in enumerate(flow["steps"], start=1):
        action = step.get("action")
        print(f"🔄 Step {i}: {action}")

        if _finish_if_result(with_exp=False, label="✅ Battle selesai, result screen muncul (awal step)"):
            return True

        if action not in NO_WAIT_ACTIONS:
            if not wait_for_auto_button(timeout=20, debug=False):
                continue
            time.sleep(1)

        handler = ACTIONS.get(action)
        if handler:
            handler(step, refresh)

        if _finish_if_result(with_exp=True):
            return True

        time.sleep(1)  # delay antar step biar stabil

    print("✅ Semua step manual selesai → kembali ke main flow")
    click_bookmark()
    return True
