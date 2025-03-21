from bot_core import *
from sample import main

# List nama raid
raid_lu_woh = 'img/raid/raid_lu_woh.png'
raid_lumi_m3 = 'img/raid/raid_lumi_credo.png'

# Memilih raid
def select_raid(raid):
    print("Selecting the raid with the highest HP...")
    if find_and_click(raid, confidence=0.5):
        print("Raid selected, waiting for OK button...")
        time.sleep(0.5)
        start_time = time.time()
        if find_and_click('img/asset/img_pending_battle.png', confidence=0.95):
            print("Pending battle detected! Clicking OK...")
            click_ok()
            time.sleep(random.uniform(1.5, 3))
            handle_pending_battles(raid)
            return

        if find_and_click('img/asset/img_3_backup.png', confidence=0.95):
            print("Backup limit reached, waiting 1 minute...")
            click_ok()
            time.sleep(random.uniform(10, 20))
            refresh_raid()
            return

        if find_and_click('img/asset/img_raid_battle_ended.png', confidence=0.95):
            print("Raid already ended")
            click_ok()
            time.sleep(random.uniform(0.5, 0.9))
            refresh_raid()
            return

        if find_and_click('img/asset/img_raid_battle_full.png', confidence=0.95):
            print("Raid already ended")
            click_ok()
            time.sleep(random.uniform(0.5, 0.9))
            refresh_raid()
            return

        while not find_and_click('img/button/button_ok.png', confidence=0.8):
            print("OK button not found, retrying...")
            time.sleep(0.5)
            if time.time() - start_time > 5:
                print("Timeout reached: returning True")
                return
        if find_and_click('img/asset/captcha.png', confidence=0.7):
            print("⚠️ Captcha detected! Stopping bot...")
            exit()

        if find_and_click('img/asset/img_pending_battle.png', confidence=0.8):
            print("Pending battle detected! Clicking OK...")
            click_ok()
            time.sleep(random.uniform(1, 2))
            handle_pending_battles(raid)
            return

        if find_and_click('img/asset/img_raid_battle_ended_2.png'):
            print("Pending battle detected! Clicking OK...")
            click_ok()
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


def quick_summon():
    print("Waiting for quick summon button...")
    start_time = time.time()
    while True:
        if result_battle():
            return main()
        if find_and_click('img/asset/img_waiting_for_last_turn.png', confidence=0.8):
            print("Result battle detected! Jumping to bookmark.")
            click_ok()
            continue
        if find_and_click('img/button/button_quick.png', confidence=0.7) or find_and_click('img/button/button_quick_v2.png', confidence=0.7):
            print("Quick summon button not found, retrying...")
            time.sleep(0.5)
            break

    print("Quick summon button found! Waiting 3 seconds before clicking...")
    time.sleep(2.3)
    pyautogui.click()
    time.sleep(0.5)
    print("Clicking back button after quick summon...")
    find_and_click('img/button/button_back.png', confidence=0.8)
    time.sleep(random.uniform(1, 2))

def result_battle():
    if find_and_click('img/asset/img_result_battle.png', confidence=0.8) or find_and_click('img/asset/img_result_battle_2.png', confidence=0.8):
        print("Result battle detected! Jumping to bookmark.")
        find_and_click('img/asset/bookmark.png', confidence=0.8)
        return

