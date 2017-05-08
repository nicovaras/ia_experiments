from utils import get_window_position
from mss import mss
import numpy as np
import cv2
import pytesser

if __name__ == "__main__":
    sct = mss()
    mon = get_window_position("Hitori")
    pixels = sct.get_pixels(mon)
    im = np.fromstring(pixels, np.uint8).reshape(mon['height'], mon['width'], 3)
    nums = [list(l) for l in pytesser.iplimage_to_string(im).split('\n') if len(l) == 5]
    print nums
