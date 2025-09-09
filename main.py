from core.page_checker import check_backup_request
from core.raid_menu_handler import *
from core.battle import handle_battle
from utils.config_utils import load_config


def main():
    print("🚀 Bot start...")
    cfg = load_config()
    first_mode = cfg.get("mode", "raid").split(",")[0].strip().lower()
    # print(first_mode)

    # cek backup request hanya kalau bukan solo
    if first_mode != "solo":
        if not check_backup_request():
            return  # langsung stop kalau gagal

    while True:
        if first_mode == "event":
            ok = ensure_event_tab()
            if not ok:
                continue

        if first_mode == "raid":
            ok = ensure_raid_tab()
            if not ok:
                continue

        if first_mode == "solo":
            ok = ensure_solo_tab()
            if not ok:
                continue

        handle_battle()


if __name__ == "__main__":
    main()
