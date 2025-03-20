import cv2 as cv
import numpy as np
import pyautogui
import time
import random
from bot_core import *


# Memilih raid
def select_raid(raid):
    print("Selecting the raid with the highest HP...")
    if find_and_click(raid, confidence=0.7):
        print("Raid selected, waiting for OK button...")
        time.sleep(0.3)
        if find_and_click('img/asset/img_pending_battle.png', confidence=0.8):
            print("Pending battle detected! Clicking OK...")
            click_ok()
            time.sleep(random.uniform(1.5, 3))
            handle_pending_battles(raid)
            return

        if find_and_click('img/asset/img_3_backup.png', confidence=0.8):
            print("Backup limit reached, waiting 1 minute...")
            click_ok()
            time.sleep(random.uniform(10, 20))
            refresh_raid()
            return

        while not find_and_click('img/button/button_ok.png', confidence=0.8):
            print("OK button not found, retrying...")
            time.sleep(0.5)
        if find_and_click('img/asset/captcha.png', confidence=0.8):
            print("⚠️ Captcha detected! Stopping bot...")
            exit()
        if find_and_click('img/asset/img_raid_battle_ended_2.png'):
            find_and_click('img/asset/bookmark.png', confidence=0.8)
            return
        print("OK button found! Entering battle...")
        time.sleep(random.uniform(1, 3))
        return True

    print("No suitable raid found, refreshing!")
    return False

# Pencet tombol ok
def click_ok():
    find_and_click('img/button/button_ok.png')
    time.sleep(random.uniform(1.5, 3))

# Tombol refresh raid
def refresh_raid():
    print("Refreshing the raid list...")
    find_and_click('img/button/button_refresh.png', confidence=0.8)
    time.sleep(random.uniform(0.5, 1))