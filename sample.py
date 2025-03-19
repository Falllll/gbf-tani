import time
import random
from module_tani import find_and_click, handle_notifications, select_raid, refresh_raid

def main():
    while True:
        # Handle notifications first
        handle_notifications()

        # Cek dan pilih raid dengan HP di atas 50% dan prioritaskan yang tertinggi
        raid_found = select_raid()

        if raid_found:
            print("Raid selected successfully!")
        else:
            print("No suitable raid found (all below 50%), refreshing...")
            refresh_raid()

        time.sleep(random.uniform(0.5, 1))

if __name__ == "__main__":
    main()