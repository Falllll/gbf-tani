import cv2 as cv
import numpy as np
import pyautogui
import time


def find_and_click(target_path, confidence=0.8):
    screen = pyautogui.screenshot()
    screen = cv.cvtColor(np.array(screen), cv.COLOR_RGB2BGR)

    target = cv.imread(target_path, cv.IMREAD_UNCHANGED)

    # Kalau gambar target punya alpha channel (4 channel), buang channel alpha
    if target.shape[2] == 4:
        target = target[:, :, :3]

    # Pastikan format sama (convert ke grayscale)
    screen_gray = cv.cvtColor(screen, cv.COLOR_BGR2GRAY)
    target_gray = cv.cvtColor(target, cv.COLOR_BGR2GRAY)

    # Pencocokan gambar
    result = cv.matchTemplate(screen_gray, target_gray, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    if max_val >= confidence:
        print(f"Found {target_path} with confidence {max_val}")
        x, y = max_loc
        pyautogui.click(x + target.shape[1] // 2, y + target.shape[0] // 2)
        return True
    else:
        print(f"{target_path} not found.")
        return False


def select_raid():
    print("Selecting the raid with the highest HP...")
    if find_and_click('img/raid_akasha.png', confidence=0.7):
        return True
    print("No high HP raid found.")
    return False


def refresh_raid():
    print("Refreshing the raid list...")
    find_and_click('img/button_refresh.png', confidence=0.8)
    time.sleep(2)


def attack_button():
    print("Pressing the attack button...")
    find_and_click('img/button_attack.png', confidence=0.8)


def handle_no_available_raid():
    print("Checking if there are no available raids...")
    if find_and_click('img/img_no_available_raid.png', confidence=0.8):
        print("No raids available, refreshing...")
        refresh_raid()
        return True
    return False


def main():
    while True:
        # Cek kondisi tidak ada raid
        if handle_no_available_raid():
            continue

        # Cek raid dengan HP tertinggi di atas 50%
        if select_raid():
            attack_button()
            time.sleep(5)
        else:
            print("No suitable raid found, refreshing...")
            refresh_raid()
            time.sleep(2)


if __name__ == "__main__":
    main()