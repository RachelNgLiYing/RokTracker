import numpy as np
import cv2

def get_cv2_image_from_device(device):
    screenshot = device.screencap()
    numpy_array =  np.frombuffer(screenshot, np.byte)
    return cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)

def resize_emulator(device):
    device.shell('wm size 1600x900')
    device.shell('wm density 450')
    device.shell('input keyevent KEYCODE_POWER')
    device.shell('input keyevent KEYCODE_WAKEUP')
