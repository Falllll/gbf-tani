from module_tani import *
from sample import main


def attack():
    print("Waiting for attack button...")
    start_time = time.time()
    while True:
        if result_battle():
            return main()
        if find_and_click('img/asset/img_waiting_for_last_turn.png', confidence=0.8):
            print("Result battle detected! Jumping to bookmark.")
            click_ok()
            continue
        if find_and_click('img/button/button_attack.png', confidence=0.8):
            print("Attack button found, clicking...")
            time.sleep(0.3)
            pyautogui.click()
            time.sleep(0.5)
            break
        if time.time() - start_time > 5:
            print("Timeout reached: returning True")
            return
        print("Attack button or result not found, retrying...")
        time.sleep(0.5)

    print("Clicking back after attack...")
    find_and_click('img/button/button_back.png', confidence=0.8)
    time.sleep(0.5)


def final_attack():
    print("Final attack check...")
    start_time = time.time()
    while True:
        if result_battle():
            return main()
        if find_and_click('img/asset/img_waiting_for_last_turn.png', confidence=0.8):
            print("Result battle detected! Jumping to bookmark.")
            click_ok()
            continue
        if find_and_click('img/button/button_attack.png', confidence=0.8):
            print("Attack button found again, clicking...")
            time.sleep(0.3)
            pyautogui.click()
            time.sleep(0.5)
            find_and_click('img/asset/bookmark.png', confidence=0.8)
            return

        if time.time() - start_time > 5:
            print("Timeout reached: returning True")
            return

        print("Attack button or result not found, retrying...")
        time.sleep(0.5)

# DARK

def eustace_3():
    print("Waiting for avatar or result...")
    start_time = time.time()
    while True:
        if result_battle():
            return main()
        if find_and_click('img/asset/img_waiting_for_last_turn.png', confidence=0.8):
            print("Result battle detected! Jumping to bookmark.")
            click_ok()
            continue

        if find_avatar('eustace'):
            break
        if time.time() - start_time > 5:
            print("Timeout reached: returning True")
            return

    print("Waiting for skill to appear...")
    while not find_and_click('img/skill/eustace/dark_s3.png', confidence=0.8):
        print("Skill not found, retrying...")
        time.sleep(0.5)

    print("Skill found, clicking!")
    time.sleep(0.5)
    find_and_click('img/button/button_back.png', confidence=0.8)

def freezie_2():
    print("Waiting for avatar or result...")
    start_time = time.time()
    while True:
        if result_battle():
            return main()
        if find_and_click('img/asset/img_waiting_for_last_turn.png', confidence=0.8):
            print("Result battle detected! Jumping to bookmark.")
            click_ok()
            continue

        if find_avatar('freezie'):
            break
        if time.time() - start_time > 5:
            print("Timeout reached: returning True")
            return

    print("Waiting for skill to appear...")
    while not find_and_click('img/skill/freezie/dark_s2.png', confidence=0.8):
        print("Skill not found, retrying...")
        time.sleep(0.5)

    print("Skill found, clicking!")
    time.sleep(0.5)
    find_and_click('img/button/button_back.png', confidence=0.8)

def tyra_3_2():
    print("Waiting for avatar or result...")
    start_time = time.time()
    while True:
        if result_battle():
            return main()
        if find_and_click('img/asset/img_waiting_for_last_turn.png', confidence=0.8):
            print("Result battle detected! Jumping to bookmark.")
            click_ok()
            continue

        if find_avatar('tyra'):
            break
        if time.time() - start_time > 5:
            print("Timeout reached: returning True")
            return

    print("Waiting for skill to appear...")
    while not find_and_click('img/skill/tyra/dark_s3.png', confidence=0.8):
        print("Skill not found, retrying...")
        time.sleep(0.5)
    print("Skill found, clicking!")
    time.sleep(0.5)

    while not find_and_click('img/skill/tyra/dark_s2.png', confidence=0.8):
        print("Skill not found, retrying...")
        time.sleep(0.5)

    print("Skill found, clicking!")
    time.sleep(0.5)
    time.sleep(2)
    find_and_click('img/button/button_back.png', confidence=0.8)

def y_ilsa_1():
    print("Waiting for avatar or result...")
    start_time = time.time()
    while True:
        if result_battle():
            return main()
        if find_and_click('img/asset/img_waiting_for_last_turn.png', confidence=0.8):
            print("Result battle detected! Jumping to bookmark.")
            click_ok()
            continue

        if find_avatar('ilsa'):
            break
        if time.time() - start_time > 5:
            print("Timeout reached: returning True")
            return

    print("Waiting for skill to appear...")
    while not find_and_click('img/skill/ilsa/dark_s1.png', confidence=0.8):
        print("Skill not found, retrying...")
        time.sleep(0.5)

    print("Skill found, clicking!")
    time.sleep(0.5)
    find_and_click('img/button/button_back.png', confidence=0.8)