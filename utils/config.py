# utils/config.py
import json
import os

# Tentukan path file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
DATA_FILE   = os.path.join(BASE_DIR, "data.json")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
MANUAL_FILE = os.path.join(BASE_DIR, "manual.json")
BACK_BUTTON = os.path.join(ASSETS_DIR, "button", "back.png")
SKILL_BAR_TEMPLATE = os.path.join(ASSETS_DIR, "party", "skill.png")


# === Baca config.json ===
with open(CONFIG_FILE, "r", encoding="utf-8") as cfg:
    config_data = json.load(cfg)

# Variabel terpisah untuk setiap properti dari config.json
raid_id = config_data.get("raid_id")
mode = config_data.get("mode")
setup = config_data.get("setup")

# === Baca data.json ===
with open(DATA_FILE, "r", encoding="utf-8") as df:
    data_json = json.load(df)

# Ambil semua raid_list dari data.json
raid_list = data_json.get("raid_list", [])

# Pisahkan atribut dari raid pertama sebagai contoh
# (Jika ingin semua raid dipecah, bisa loop dan simpan dalam struktur terpisah)
if raid_list:
    # Contoh: ambil raid berdasarkan ID dari config
    selected_raid = next((r for r in raid_list if r["id"] == raid_id), None)

    if selected_raid:
        raid_name = selected_raid.get("name")
        raid_source = selected_raid.get("source")
        raid_mode = selected_raid.get("mode")
        raid_grid = selected_raid.get("grid")
        raid_intro = selected_raid.get("intro")
        raid_participant = selected_raid.get("participant")
        raid_type = selected_raid.get("type")
    else:
        raid_name = raid_source = raid_mode = raid_grid = raid_intro = raid_participant = raid_type = None
else:
    selected_raid = None
    raid_name = raid_source = raid_mode = raid_grid = raid_intro = raid_participant = raid_type = None

# Debugging
# if __name__ == "__main__":
#     print("=== CONFIG.JSON ===")
#     print(f"raid_id      : {raid_id}")
#     print(f"mode         : {mode}")
#     print(f"hp_priority  : {hp_priority}\n")
#
#     print("=== DATA.JSON ===")
#     if selected_raid:
#         print(f"Selected Raid: {raid_name}")
#         print(f"Source       : {raid_source}")
#         print(f"Mode         : {raid_mode}")
#         print(f"Grid         : {raid_grid}")
#         print(f"Intro        : {raid_intro}")
#         print(f"Participant  : {raid_participant}")
#         print(f"Type         : {raid_type}")
#     else:
#         print("Raid ID tidak ditemukan.")
