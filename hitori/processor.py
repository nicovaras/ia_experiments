import cv2
from common import pytesser


class HitoriProcessor(object):

    def __init__(self, image):
        self.image = image
        self.bounding_rects = None

    def find_contours(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, self.image = cv2.threshold(self.image, 60, 255, 1)
        _, contours, _ = cv2.findContours(self.image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def delete_number_borders(self, contours):
        contours = [cnt for cnt in contours if cv2.contourArea(cnt) == cv2.contourArea(contours[1])]
        self.bounding_rects = [cv2.boundingRect(c) for c in contours][::-1]
        cv2.drawContours(self.image, contours, -1, (0, 0, 0), 3)

    def preprocess_image(self):
        contours = sorted(self.find_contours(), key=cv2.contourArea, reverse=True)
        x, y, w, h = cv2.boundingRect(contours[0])
        self.delete_number_borders(contours)
        self.image = self.image[y + 2:y + h - 2, x + 2:x + w - 2]

    def get_numbers_from_ocr(self):
        nums = pytesser.iplimage_to_string(
            self.image, psm=11, config="tessedit_char_whitelist=0123456789").strip().split()
        return [list(x) for x in nums]

    def detect_numbers(self):
        self.preprocess_image()
        return self.get_numbers_from_ocr()
