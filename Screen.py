from PIL import ImageGrab, Image
import cv2
import numpy
import pyautogui
import time
from ImageLoader import ImageLoader
import win32api
import win32gui


class Screen:
    _delay = 0.3
    _imageLoader = ImageLoader('image/')
    _skills = ImageLoader('image/skills/')

    def __init__(self):
        t = ImageGrab.grab().convert("RGB")
        self.screen = cv2.cvtColor(numpy.array(t), cv2.COLOR_RGB2BGR)

    def fight(self):
        is_final_stage = False
        if self.chances_of('3_3') > max(self.chances_of('2_3'), self.chances_of('1_3')):
            print '3-3'
            is_final_stage = True
        elif self.chances_of('2_3') > max(self.chances_of('3_3'), self.chances_of('1_3')):
            print '2-3'
        else:
            print '1-3'

        if is_final_stage:
            for key in self._skills.get_all():
                while self.have(key, loader=self._skills):
                    self.click_on(key, loader=self._skills)
                    time.sleep(2)
                    print 'use ' + key

        self.click_on('atk_btn')

        cards = []
        while len(cards) != 5:
            cards = []
            time.sleep(self._delay)
            self.capture()
            cards += self.find_list('buster')
            cards += self.find_list('art')
            cards += self.find_list('quick')

        for i in range(0, 3):
            x, y = cards[i]
            self._click(x, y)
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
        print name + ': ' + str(len(cards))

        return cards

    def set_delay(self, delay):
        self._delay = delay

    def capture(self):
        t = ImageGrab.grab().convert("RGB")
        self.screen = cv2.cvtColor(numpy.array(t), cv2.COLOR_RGB2BGR)

    @staticmethod
    def _click(x, y):
        handle = win32gui.GetForegroundWindow()
        x_old, y_old = win32api.GetCursorPos()
        pyautogui.click(x, y, 1)
        win32api.SetCursorPos((x_old, y_old))
        win32gui.SetForegroundWindow(handle)

    def click_on(self, name, repeat=False, loader=_imageLoader):
        p = loader.get(name)
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

        self._click(x, y)

        max_val = 1 if repeat else 0
        while max_val > 0.8:
            time.sleep(1)
            self.capture()
            res = cv2.matchTemplate(self.screen, p, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val > 0.8:
                self._click(x, y)

    def have(self, name, loader=_imageLoader):
        return self.chances_of(name, loader) > 0.8

    def chances_of(self, name, loader=_imageLoader):
        self.capture()
        p = loader.get(name)
        res = cv2.matchTemplate(self.screen, p, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        return max_val
