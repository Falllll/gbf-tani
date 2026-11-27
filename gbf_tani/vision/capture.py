# gbf_tani/vision/capture.py
import cv2
import numpy as np
import pyautogui


def screenshot():
    """Ambil screenshot layar penuh (return numpy array BGR)."""
    img = pyautogui.screenshot()
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
