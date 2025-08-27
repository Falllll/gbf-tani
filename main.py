from core.page_checker import check_backup_request
from core.event_handler import ensure_event_tab
from utils.config_utils import load_config

def main():
    print("🚀 Bot start...")
    if check_backup_request():
        cfg = load_config()
        first_mode = cfg.get("mode", "raid").split(",")[0].strip().lower()

        if first_mode == "event":
            ensure_event_tab()

if __name__ == "__main__":
    main()
