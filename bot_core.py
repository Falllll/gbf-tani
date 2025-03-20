import cv2 as cv
import numpy as np
import pyautogui
import time
import random


# CORE SECTION
# Untuk mendeteksi gambar
def find_and_click(target_path, confidence=0.8):
    screen = pyautogui.screenshot()
    screen = cv.cvtColor(np.array(screen), cv.COLOR_RGB2BGR)
    target = cv.imread(target_path, cv.IMREAD_UNCHANGED)

    if target is None:
        print(f"Error: Failed to load image {target_path}")
        return False

    if target.shape[2] == 4:
        target = target[:, :, :3]

    screen_gray = cv.cvtColor(screen, cv.COLOR_BGR2GRAY)
    target_gray = cv.cvtColor(target, cv.COLOR_BGR2GRAY)

    result = cv.matchTemplate(screen_gray, target_gray, cv.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv.minMaxLoc(result)

    if max_val >= confidence:
        print(f"Found {target_path} with confidence {max_val}")
        x, y = max_loc
        pyautogui.click(x + target.shape[1] // 2, y + target.shape[0] // 2)
        return True
    else:
        print(f"{target_path} not found.")
        return False


# Menghandle pending battle
def handle_pending_battles(raid):
    print("Handling pending battles...")
    while find_and_click(raid, confidence=0.7):
        print("Clicked on a pending raid, collecting rewards...")
        time.sleep(random.uniform(0.5, 2))
        find_and_click('img/button/button_back.png', confidence=0.8)
        time.sleep(random.uniform(0.5, 2))
    find_and_click('img/button/button_back.png', confidence=0.8)
    print("Finished collecting pending rewards, returning to main list.")