import json
import time
from utils.screenshot import (
    click_image_fullscreen,
    click_skill_relative,
    click_image_fullscreen_with_coords,
    click_summon_index,
    click_summon_button,
    click_auto_button,
    click_quick_summon_button,
    click_back_button,
    click_ok_button,
    wait_for_auto_button,  # ✅ fungsi baru
)

last_character_coords = None
last_character_position = None  # ✅ inisialisasi dulu

def main():
    global last_character_coords, last_character_position
    print("=== TEST FLOW DARI manual.json ===")

    with open("manual.json", "r", encoding="utf-8") as f:
        flow = json.load(f)
    refresh = flow.get("refresh", False)

    print("Refresh:", refresh)

    for step in flow["steps"]:
        action = step.get("action")
        target = step.get("target")
        skill_index = step.get("skill_index")

        # ✅ Cek apakah action butuh nunggu tombol auto
        if action not in ["use_skill", "use_summon"]:
            if not wait_for_auto_button(timeout=20, debug=True):
                print(f"[DEBUG] Auto button tidak muncul → skip step {action}")
                continue
            time.sleep(0.5)

        if action == "select_character":
            print(f"[DEBUG] Pilih karakter {target} (assets/party/{target}.png)")
            coords = click_image_fullscreen_with_coords(
                f"assets/party/{target}.png", debug=True
            )
            if coords:
                last_character_coords = coords
                last_character_position = target
                print(last_character_position)
            else:
                print("[DEBUG] Karakter tidak ketemu → skip")

        elif action == "use_skill":
            if last_character_coords and last_character_position:
                print(f"[DEBUG] Klik skill {skill_index} (target {target}) relatif")
                click_skill_relative(
                    last_character_coords[0],
                    last_character_coords[1],
                    skill_index,
                    last_character_position,
                    debug=True,
                )
                if refresh:
                    time.sleep(0.5)
                    click_back_button(debug=True)
            else:
                print("[DEBUG] Belum ada karakter yang dipilih → gak bisa klik skill")

        elif action == "select_summon":
            print("[DEBUG] Klik tombol summon")
            click_summon_button(debug=True)

        elif action == "quick_summon":
            print("[DEBUG] Klik tombol summon cepat")
            click_quick_summon_button(debug=True)
            if refresh:
                time.sleep(0.5)
                click_back_button(debug=True)

        elif action == "auto":
            print("[DEBUG] Klik tombol auto")
            click_auto_button(debug=True)
            if refresh:
                time.sleep(0.5)
                click_back_button(debug=True)

        elif action == "use_summon":
            summon_index = step.get("summon_index", 1)
            print(f"[DEBUG] Klik summon {summon_index}")
            click_summon_index(summon_index, debug=True)
            time.sleep(0.5)
            click_ok_button()
            if refresh:
                time.sleep(0.5)
                click_back_button(debug=True)

        elif action == "attack":
            print("[DEBUG] Klik tombol attack")
            click_image_fullscreen("assets/button/attack.png", debug=True)
            if refresh:
                time.sleep(0.5)
                click_back_button(debug=True)

        # Delay kecil antar step (optional)
        time.sleep(1)

if __name__ == "__main__":
    main()
