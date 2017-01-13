# coding=utf-8

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
    target = ImageLoader('./')
    _stop = False
    _current_stage = 0
    
    def log(self, text):
        self.window.add_text(text)

    def __init__(self, window):
        t = ImageGrab.grab().convert("RGB")
        self.screen = cv2.cvtColor(numpy.array(t), cv2.COLOR_RGB2BGR)
        self.window = window
        
        if self.have('topleft'):
            tl = self._imageLoader.get('topleft')
            res = cv2.matchTemplate(self.screen, tl, cv2.TM_CCOEFF_NORMED)

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            x1, y1 = max_loc
            rd = self._imageLoader.get('rightdown')
            res = cv2.matchTemplate(self.screen, rd, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            x2, y2 = max_loc
            # default 989
            y = y2 - y1
            self._imageLoader.y = y
            self._skills.y = y
            self._imageLoader.use_haimawan = True
            self._skills.use_haimawan = True

    def fight(self):
        c33 = self.chances_of('3_3')
        c23 = self.chances_of('2_3')
        c31 = self.chances_of('1_3')
        if c33 > max(c23, c31):
            self.log('3-3')
            self._current_stage = 3
        elif c23 > max(c33, c31):
            self.log('2-3')
            self._current_stage = 2
        else:
            self.log('1-3')
            self._current_stage = 1

        if self._current_stage == 3:
            for key in self._skills.get_all():
                while self.have(key, loader=self._skills):
                    if self._stop:
                        return
                    self.click_on(key, loader=self._skills)
                    time.sleep(2)
                    self.log('use ' + key)

        cards = []

        while len(cards) < 3:
            if self._stop:
                return
            cards = []

            if self.have('atk_btn'):
                self.click_on('atk_btn')
                time.sleep(1)

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
        self.log(name + ': ' + str(len(cards)))

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
        # see https://github.com/asweigart/pyautogui/issues/23
        try:
            pyautogui.click(x, y, 1)
        except FileNotFoundError:
            pass

        win32api.SetCursorPos((x_old, y_old))
        win32gui.SetForegroundWindow(handle)

    def click_on(self, name, repeat=False, loader=_imageLoader):
        self.log('try click ' + name)
        p = loader.get(name)
        max_val = 0
        x, y = 0, 0
        while max_val < 0.8:
            if self._stop:
                return

            self.capture()
            res = cv2.matchTemplate(self.screen, p, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            self.log(name + ' ' + str(max_val))
            x, y = max_loc
            time.sleep(self._delay)

        m, n, q = p.shape

        x += n / 2
        y += m / 2

        self._click(x, y)

        max_val = 1 if repeat else 0
        while max_val > 0.8:
            if self._stop:
                return

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
        self.log('chances of ' + name + ': ' + str(max_val))
        return max_val

    def stop(self):
        self._stop = True
        self.log("stop screen")
