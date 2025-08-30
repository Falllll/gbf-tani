from core.page_checker import check_backup_request
from core.raid_menu_handler import *
from utils.config_utils import load_config

def main():
    print("🚀 Bot start...")
    if check_backup_request():
        cfg = load_config()
        first_mode = cfg.get("mode", "raid").split(",")[0].strip().lower()

        if first_mode == "event":
            ensure_event_tab()

        if first_mode == "raid":
            ensure_raid_tab()

if __name__ == "__main__":
    main()
