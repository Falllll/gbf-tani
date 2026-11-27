import time

from gbf_tani.config import mode
from gbf_tani.flows.navigator import check_tab

MAX_RUNTIME_SECONDS = 5 * 60 * 60  # 2 jam
# MAX_RUNTIME_SECONDS = 12750


def main():
    print("🚀 Bot start...")
    first_mode = mode.split(",")[0].strip().lower()
    start_time = time.time()

    while True:
        if time.time() - start_time >= MAX_RUNTIME_SECONDS:
            print("Runtime limit reached (2 hours). Exiting.")
            break
        check_tab(first_mode)


if __name__ == "__main__":
    main()
