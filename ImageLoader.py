from PIL import ImageGrab, Image
import cv2
import numpy
import pyautogui
import PIL
import os


class ImageLoader:
    _images = {}
    _image_path = 'image//'

    def __init__(self):
        for pic in os.listdir(self._image_path):
            if pic.endswith(".png"):
                img = cv2.imread(self._image_path + pic)
                self._images[pic] = img
        pass

    def get(self, name):
        return self._images[name + '.png']
