from PIL import ImageGrab, Image
import cv2
import numpy
import pyautogui
import PIL
import time
from ImageLoader import ImageLoader


class Screen:
    _delay = 0.3
    _imageLoader = ImageLoader()

    def __init__(self):
        t = ImageGrab.grab().convert("RGB")
        self.screen = cv2.cvtColor(numpy.array(t), cv2.COLOR_RGB2BGR)

    def fight(self):
        self.click_on('atk_btn')
        time.sleep(self._delay)
        cards = []
        self.capture()
        if self.chances_of('3_3') > max(self.chances_of('2_3'), self.chances_of('1_3')):
            print '3-3'
        elif self.chances_of('2_3') > max(self.chances_of('3_3'), self.chances_of('1_3')):
            print '2-3'
        else:
            print '1-3'
        cards += self.find_list('buster')
        cards += self.find_list('art')
        cards += self.find_list('quick')

        for i in range(0, 3):
            x, y = cards[i]
            x_old, y_old = pyautogui.position()
            pyautogui.click(x, y, 1)
            pyautogui.moveTo(x_old, y_old)
            time.sleep(self._delay)

    def find_list(self, name):
        cards = []
        res = cv2.matchTemplate(self.screen, self._imageLoader.get(name), cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = numpy.where(res >= threshold)
        x = 0
        t = sorted(zip(*loc[::-1]))
        for pt in t:
            if abs(x - pt[0]) > 100 or x == 0:
                x = pt[0]
                cards.append((pt[0], pt[1]))
            else:
                continue
        print name + ' len: ' + str(len(cards))

        return cards

    def set_delay(self, delay):
        self._delay = delay

    def capture(self):
        t = ImageGrab.grab().convert("RGB")
        self.screen = cv2.cvtColor(numpy.array(t), cv2.COLOR_RGB2BGR)

    def click_on(self, name, repeat=False):

        p = self._imageLoader.get(name)
        max_val = 0
        x, y = 0, 0
        while max_val < 0.8:
            self.capture()
            res = cv2.matchTemplate(self.screen, p, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            x, y = max_loc
            time.sleep(self._delay)

        m, n, q = p.shape

        x += n / 2
        y += m / 2

        x_old, y_old = pyautogui.position()
        pyautogui.click(x, y, 1)

        max_val = 1 if repeat else 0
        while max_val > 0.8:
            self.capture()
            res = cv2.matchTemplate(self.screen, p, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            time.sleep(self._delay)
            pyautogui.click(x, y, 1)

        pyautogui.moveTo(x_old, y_old)

    def have(self, name):
        return self.chances_of(name) > 0.8

    def chances_of(self, name):
        self.capture()
        p = self._imageLoader.get(name)
        res = cv2.matchTemplate(self.screen, p, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        return max_val
