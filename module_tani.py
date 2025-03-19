import cv2 as cv
import numpy as np
import pyautogui
import time
import random

# Load reference images for HP bar comparison
hp_bar_full = cv.imread('img/asset/img_hp_bar_100.png', cv.IMREAD_GRAYSCALE)
hp_bar_empty = cv.imread('img/asset/img_hp_bar_0.png', cv.IMREAD_GRAYSCALE)

# Ensure images loaded correctly
if hp_bar_full is None or hp_bar_empty is None:
    print("Error loading HP bar reference images.")


def find_and_click(target_path, confidence=0.8):
    screen = pyautogui.screenshot()
    screen = cv.cvtColor(np.array(screen), cv.COLOR_RGB2BGR)
    target = cv.imread(target_path, cv.IMREAD_UNCHANGED)

    if target is None:
        print(f"Error: Failed to load image {target_path}")
        return False

    if target.ndim == 2:
        target_gray = target
    else:
        target_gray = cv.cvtColor(target, cv.COLOR_BGR2GRAY)

    screen_gray = cv.cvtColor(screen, cv.COLOR_BGR2GRAY)

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


# Calculate HP percentage using image comparison
def get_hp_percentage_v2(hp_bar_region):
    screen = pyautogui.screenshot(region=hp_bar_region)
    screen_gray = cv.cvtColor(np.array(screen), cv.COLOR_RGB2GRAY)

    # Compare with reference images
    similarity_full = cv.matchTemplate(screen_gray, hp_bar_full, cv.TM_CCOEFF_NORMED).max()
    similarity_empty = cv.matchTemplate(screen_gray, hp_bar_empty, cv.TM_CCOEFF_NORMED).max()

    # Calculate HP percentage based on similarity
    if similarity_full > similarity_empty:
        return min(100, (similarity_full / (similarity_full + similarity_empty)) * 100)
    else:
        return max(0, (1 - similarity_empty / (similarity_full + similarity_empty)) * 100)


def select_raid():
    print("Selecting the raid with HP above 50%...")

    raid_positions = [
        {'image': 'img/raid/raid_akasha.png', 'hp_region': (800, 350, 100, 20)},
        {'image': 'img/raid/raid_baha.png', 'hp_region': (800, 450, 100, 20)},
        {'image': 'img/raid/raid_faa.png', 'hp_region': (800, 550, 100, 20)},
    ]

    best_raid = None
    highest_hp = 0

    for raid in raid_positions:
        if find_and_click(raid['image'], confidence=0.7):
            hp_percent = get_hp_percentage_v2(raid['hp_region'])
            print(f"Raid {raid['image']} HP: {hp_percent:.2f}%")
            if hp_percent > 50 and hp_percent > highest_hp:
                highest_hp = hp_percent
                best_raid = raid

    if best_raid:
        print(f"Selecting raid {best_raid['image']} with HP: {highest_hp:.2f}%")
        find_and_click(best_raid['image'], confidence=0.7)
        while not find_and_click('img/button/button_ok.png', confidence=0.8):
            print("OK button not found, retrying...")
            time.sleep(0.5)
        print("OK button found! Entering battle...")
        time.sleep(random.uniform(1, 3))
        return True

    print("No suitable raid found, refreshing!")
    return False
