import json

CONFIG_PATH = "config.json"

def load_config(path: str = CONFIG_PATH) -> dict:
    """
    Load konfigurasi dari config.json
    Return dict (default kosong kalau gagal).
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Gagal baca config: {e}")
        return {}
