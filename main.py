import cv2 as cv
import numpy as np
import pyautogui
import time
import random

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

def handle_pending_battles():
    print("Handling pending battles...")
    while find_and_click('img/raid_akasha_result.png', confidence=0.7):
        print("Clicked on a pending raid, collecting rewards...")
        time.sleep(random.uniform(3, 4))
        find_and_click('img/button_back.png', confidence=0.8)
        time.sleep(random.uniform(2, 3))
    find_and_click('img/button_back.png', confidence=0.8)
    print("Finished collecting pending rewards, returning to main list.")

def click_ok():
    find_and_click('img/button_ok.png')
    time.sleep(random.uniform(1.5, 3))

def handle_notifications():
    notifications = [
        ('img/img_raid_battle_full.png', "Raid full detected!"),
        ('img/img_raid_battle_ended.png', "Raid ended detected!"),
    ]

    for img_path, message in notifications:
        if find_and_click(img_path, confidence=0.8):
            print(message)
            click_ok()
            print("Refreshing the raid list...")
            find_and_click('img/button_refresh.png', confidence=0.8)
            time.sleep(random.uniform(1.5, 3))

    if find_and_click('img/img_3_backup.png', confidence=0.8):
        print("Backup limit reached, waiting 1 minute...")
        click_ok()
        time.sleep(random.uniform(50, 60))

    if find_and_click('img/img_pending_battle.png', confidence=0.8):
        print("Pending battle detected! Clicking OK...")
        click_ok()
        time.sleep(random.uniform(1.5, 3))
        handle_pending_battles()
        return True

    return False

def select_raid():
    print("Selecting the raid with the highest HP...")
    if find_and_click('img/raid_akasha.png', confidence=0.7):
        print("Raid selected, waiting for OK button...")
        while not find_and_click('img/button_ok.png', confidence=0.8):
            print("OK button not found, retrying...")
            time.sleep(0.5)
        print("OK button found! Entering battle...")
        time.sleep(random.uniform(1, 3))
        return True

    print("No suitable raid found, refreshing!")
    return False

def refresh_raid():
    print("Refreshing the raid list...")
    find_and_click('img/button_refresh.png', confidence=0.8)
    time.sleep(random.uniform(0.5, 1))

def wait_for_battle():
    print("Waiting for quick summon button...")
    while True:
        if find_and_click('img/img_result_battle.png', confidence=0.8):
            print("Result battle detected! Jumping to bookmark.")
            find_and_click('img/bookmark.png', confidence=0.8)
            return
        if find_and_click('img/img_waiting_for_last_turn.png', confidence=0.8):
            print("Result battle detected! Jumping to bookmark.")
            click_ok()
            continue
        if find_and_click('img/button_quick.png', confidence=0.8):
            print("Quick summon button not found, retrying...")
            time.sleep(0.5)
            break

    print("Quick summon button found! Waiting 3 seconds before clicking...")
    time.sleep(2.3)
    pyautogui.click()
    time.sleep(0.5)
    print("Clicking back button after quick summon...")
    find_and_click('img/button_back.png', confidence=0.8)
    time.sleep(random.uniform(1, 2))

    # Cek paralel antara avatar atau result battle
    print("Waiting for avatar or result...")
    while True:
        if find_and_click('img/img_result_battle.png', confidence=0.8):
            print("Result battle detected! Jumping to bookmark.")
            find_and_click('img/bookmark.png', confidence=0.8)
            return
        if find_and_click('img/img_waiting_for_last_turn.png', confidence=0.8):
            print("Result battle detected! Jumping to bookmark.")
            click_ok()
            continue
        if find_and_click('img/avatar_y_ilsa.png', confidence=0.8):
            print("Avatar found! Waiting 3 seconds...")
            time.sleep(2.3)
            pyautogui.click()
            break
        print("Avatar or result not found, retrying...")
        time.sleep(0.5)

    print("Waiting for skill to appear...")
    while not find_and_click('img/y_ilsa_s1.png', confidence=0.8):
        print("Skill not found, retrying...")
        time.sleep(0.5)

    print("Skill found, clicking!")
    time.sleep(0.5)
    find_and_click('img/button_back.png', confidence=0.8)

    print("Waiting for attack button...")
    while True:
        if find_and_click('img/img_result_battle.png', confidence=0.8):
            print("Result battle detected! Jumping to bookmark.")
            find_and_click('img/bookmark.png', confidence=0.8)
            return
        if find_and_click('img/img_waiting_for_last_turn.png', confidence=0.8):
            print("Result battle detected! Jumping to bookmark.")
            click_ok()
            continue
        if find_and_click('img/button_attack.png', confidence=0.8):
            print("Attack button found, clicking...")
            time.sleep(0.3)
            pyautogui.click()
            time.sleep(0.5)
            break
        print("Attack button or result not found, retrying...")
        time.sleep(0.5)

    print("Clicking back after attack...")
    find_and_click('img/button_back.png', confidence=0.8)
    time.sleep(0.5)

    print("Waiting for summon...")
    while True:
        if find_and_click('img/img_result_battle.png', confidence=0.8):
            print("Result battle detected! Jumping to bookmark.")
            find_and_click('img/bookmark.png', confidence=0.8)
            return
        if find_and_click('img/img_waiting_for_last_turn.png', confidence=0.8):
            print("Result battle detected! Jumping to bookmark.")
            click_ok()
            continue
        if find_and_click('img/img_summon.png', confidence=0.8):
            print("Summon button found, waiting 3 seconds...")
            time.sleep(2.3)
            pyautogui.click()
            time.sleep(0.5)
            find_and_click('img/summon_zirnitra.png', confidence=0.8)
            break
        print("Summon or result not found, retrying...")
        time.sleep(0.5)

    print("Waiting for OK button after summon...")
    while True:
        if find_and_click('img/img_result_battle.png', confidence=0.8):
            print("Result battle detected! Jumping to bookmark.")
            find_and_click('img/bookmark.png', confidence=0.8)
            return
        if find_and_click('img/img_waiting_for_last_turn.png', confidence=0.8):
            print("Result battle detected! Jumping to bookmark.")
            click_ok()
            continue
        if find_and_click('img/button_ok.png', confidence=0.8):
            print("OK button found, clicking...")
            pyautogui.click()
            break
        print("OK button or result not found, retrying...")
        time.sleep(0.5)

    print("Clicking back after OK...")
    find_and_click('img/button_back.png', confidence=0.8)
    time.sleep(0.5)

    print("Final attack check...")
    while True:
        if find_and_click('img/img_result_battle.png', confidence=0.8):
            print("Result battle detected! Jumping to bookmark.")
            find_and_click('img/bookmark.png', confidence=0.8)
            return
        if find_and_click('img/img_waiting_for_last_turn.png', confidence=0.8):
            print("Result battle detected! Jumping to bookmark.")
            click_ok()
            continue
        if find_and_click('img/button_attack.png', confidence=0.8):
            print("Attack button found again, clicking...")
            time.sleep(0.3)
            pyautogui.  click()
            time.sleep(0.5)
            find_and_click('img/bookmark.png', confidence=0.8)
            break
        print("Attack button or result not found, retrying...")
        time.sleep(0.5)

def main():
    while True:
        handle_notifications()
        if select_raid():
            wait_for_battle()
        else:
            print("No suitable raid found, refreshing...")
            refresh_raid()
        time.sleep(random.uniform(0.5, 1))

if __name__ == "__main__":
    main()