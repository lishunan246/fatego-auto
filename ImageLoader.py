import cv2
import os


class ImageLoader:
    _postfix = '.png'
    delta_y = 989.0
    y = 989.0
    use_haimawan = False

    def __init__(self, path):
        self.images = {}
        self._image_path = path

        for pic in os.listdir(self._image_path):
            if pic.endswith(".png"):
                img = cv2.imread(self._image_path + pic)

                self.images[pic] = img

    def get(self, name):
        img = self.images[name + self._postfix]
        if self.use_haimawan:
            x, y, z = img.shape
            t = self.y / self.delta_y
            img = cv2.resize(img, (int(y * t), int(x * t)), fx=t, fy=t)

        return img

    def get_all(self):
        return map(lambda x: x[:-len(self._postfix)], self.images.keys())
