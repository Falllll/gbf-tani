import time

from gbf_tani.config import mode, timer, timer_seconds
from gbf_tani.flows.navigator import check_tab


def main():
    print("🚀 Bot start...")
    if timer:
        print(f"⏱️ Timer aktif: bot berhenti setelah {timer_seconds / 3600:g} jam")
    start_time = time.time()

    while True:
        if timer and time.time() - start_time >= timer_seconds:
            print(f"Runtime limit reached ({timer_seconds / 3600:g} hours). Exiting.")
            break
        check_tab(mode)


if __name__ == "__main__":
    main()
