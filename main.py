from core.page import check_tab
from utils.config import mode

def main():
    print("🚀 Bot start...")
    first_mode = mode.split(",")[0].strip().lower()

    while True:  # Loop utama
        check_tab(first_mode)

if __name__ == "__main__":
    main()
