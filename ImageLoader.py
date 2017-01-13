import cv2
import os
from GameStatus import GameStatus


class ImageLoader:
    _postfix = '.png'
    delta_y = 989.0

    def __init__(self, path, need_scale=True):
        self.images = {}
        self._image_path = path
        self.need_scale = need_scale
        for pic in os.listdir(self._image_path):
            if pic.endswith(".png"):
                img = cv2.imread(self._image_path + pic)

                self.images[pic] = img

    def get(self, name):
        img = self.images[name + self._postfix]
        if self.need_scale and GameStatus().use_Droid4X:
            x, y, z = img.shape
            t = GameStatus().y / self.delta_y
            img = cv2.resize(img, (int(y * t), int(x * t)), fx=t, fy=t)

        return img

    def get_all(self):
        return map(lambda x: x[:-len(self._postfix)], self.images.keys())
