import json

CONFIG_PATH = "config.json"
REGISTRY_PATH = "registry.json"

def _load_json(path: str) -> dict:
    """Helper untuk load file JSON jadi dict"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Gagal baca {path}: {e}")
        return {}

# =======================
# CONFIG.JSON
# =======================
def load_config(path: str = CONFIG_PATH) -> dict:
    return _load_json(path)

def get_config(key: str, default=None, path: str = CONFIG_PATH):
    cfg = load_config(path)
    return cfg.get(key, default)

# =======================
# REGISTRY.JSON
# =======================
def load_registry(path: str = REGISTRY_PATH) -> dict:
    return _load_json(path)

def get_raid_source_by_id(raid_id: str, registry: dict = None) -> str | None:
    """Cari source image berdasarkan raid_id"""
    if registry is None:
        registry = load_registry()
    for _, data in registry.items():
        if data.get("id") == raid_id:
            return data.get("source")
    return None
