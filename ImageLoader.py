from PIL import ImageGrab, Image
import cv2
import numpy
import pyautogui
import PIL
import os


class ImageLoader:

    _postfix = '.png'

    def __init__(self, path):
        self.images = {}
        self._image_path = path
        for pic in os.listdir(self._image_path):
            if pic.endswith(".png"):
                img = cv2.imread(self._image_path + pic)
                self.images[pic] = img

    def get(self, name):
        return self.images[name + self._postfix]

    def get_all(self):
        return map(lambda x: x[:-len(self._postfix)], self.images.keys())
