# gbf_tani/config.py
"""Baca config.json + data.json sekali saat import, expose sebagai konstanta modul."""
import json
import os

# Root project (folder yang berisi main.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
DATA_FILE = os.path.join(BASE_DIR, "data.json")
MANUAL_FILE = os.path.join(BASE_DIR, "manual.json")


def _load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# === config.json ===
config_data = _load_json(CONFIG_FILE)

raid_id = config_data.get("raid_id")
mode = config_data.get("mode")
setup = config_data.get("setup")

# === data.json ===
data_json = _load_json(DATA_FILE)
raid_list = data_json.get("raid_list", [])

# Raid yang dipilih berdasarkan raid_id di config.json (None kalau tidak ketemu)
selected_raid = next((r for r in raid_list if r["id"] == raid_id), None)

_raid = selected_raid or {}
raid_name = _raid.get("name")
raid_source = _raid.get("source")
raid_mode = _raid.get("mode")
raid_grid = _raid.get("grid")
raid_intro = _raid.get("intro")
raid_participant = _raid.get("participant")
raid_type = _raid.get("type")
