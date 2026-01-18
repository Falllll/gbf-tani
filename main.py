import time

from core.page import check_tab
from utils.config import mode


def main():
    print("ĐYs? Bot start...")
    first_mode = mode.split(",")[0].strip().lower()
    start_time = time.time()
    max_runtime_seconds = 3 * 60 * 60

    while True:  # Loop utama
        if time.time() - start_time >= max_runtime_seconds:
            print("Runtime limit reached (2 hours). Exiting.")
            break
        check_tab(first_mode)


if __name__ == "__main__":
    main()
