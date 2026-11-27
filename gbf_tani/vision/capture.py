# gbf_tani/vision/capture.py
import cv2
import numpy as np
import pyautogui

from gbf_tani import context


def screenshot():
    """Screenshot (numpy array BGR). 1 akun: layar penuh. Multi: cuma area jendela akun ini."""
    region = context.region()
    if region is None:
        # --- 1 akun (perilaku lama, tidak diubah) ---
        img = pyautogui.screenshot()
    else:
        # --- multi akun ---
        with context.INPUT_LOCK:
            img = pyautogui.screenshot(region=region)
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
