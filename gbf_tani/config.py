# gbf_tani/config.py
"""Baca config.json + data.json sekali saat import, expose sebagai konstanta modul."""
import json
import math
import os
import re

# Root project (folder yang berisi main.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
DATA_FILE = os.path.join(BASE_DIR, "data.json")
MANUAL_FILE = os.path.join(BASE_DIR, "manual.json")


def _load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _require_bool(key):
    """Ambil key boolean dari config.json. Kalau tidak ada / bukan true-false → stop dengan pesan jelas."""
    value = config_data.get(key)
    if not isinstance(value, bool):
        raise SystemExit(
            f'❌ config.json: "{key}" harus true atau false (tanpa tanda kutip), '
            f"sekarang: {json.dumps(value)}"
        )
    return value


def _require_positive_int(key):
    """Ambil bilangan bulat ≥ 1 dari config.json (tanpa tanda kutip)."""
    value = config_data.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise SystemExit(
            f'❌ config.json: "{key}" harus angka bulat 1 atau lebih (tanpa tanda kutip), '
            f"sekarang: {json.dumps(value)}"
        )
    return value


# Angka, atau perkalian angka: "18000", "5 * 60 * 60", "1.5 * 60 * 60"
_NUMBER = r"\d+(?:\.\d+)?"
_PRODUCT_RE = re.compile(rf"^\s*{_NUMBER}(?:\s*\*\s*{_NUMBER})*\s*$")


def _require_seconds(key):
    """
    Ambil durasi (detik) dari config.json. Boleh angka (18000) atau
    rumus perkalian dalam string ("5 * 60 * 60"). Harus lebih dari 0.
    """
    value = config_data.get(key)

    if isinstance(value, str) and _PRODUCT_RE.match(value):
        seconds = math.prod(float(part) for part in value.split("*"))
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        seconds = float(value)
    else:
        seconds = None

    if seconds is None or seconds <= 0:
        raise SystemExit(
            f'❌ config.json: "{key}" harus angka detik lebih dari 0, '
            f'contoh: 3600 atau "1 * 60 * 60" — sekarang: {json.dumps(value)}'
        )
    return seconds


# === config.json ===
config_data = _load_json(CONFIG_FILE)

# Urutan sama dengan config.json: raid → battle → akun → sesi

# Raid & mode
raid_id = config_data.get("raid_id")
finder = _require_bool("finder")              # true → mode finder, false → mode solo

# Battle
full_auto = _require_bool("full_auto")        # true → full auto, false → manual (manual.json)
fast_refresh = _require_bool("fast_refresh")  # FA saja: true → klik back 0.5–1 detik setelah auto, tanpa nunggu attack hilang

# Akun
accounts = _require_positive_int("accounts")  # jumlah akun = jumlah jendela browser game

# Sesi
timer = _require_bool("timer")                # true → berhenti setelah timer_seconds waktu jalan, false → jalan terus
timer_seconds = _require_seconds("timer_seconds") if timer else None
humanizer = _require_bool("humanizer")        # true → jalan 30–60 menit, istirahat 30–60 menit, diulang

# Mode yang dipakai navigator
mode = "finder" if finder else "solo"

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
