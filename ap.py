from PIL import ImageGrab, Image
import cv2
import numpy
import pyautogui
import PIL

image_path = 'image//'

img = ImageGrab.grab().convert("RGB")
img = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)

atk_btn = cv2.imread(image_path + "atk_btn.png")
quick = cv2.imread(image_path + "quick.png")
art = cv2.imread(image_path + "art.png")
buster = cv2.imread(image_path + "buster.png")
lancer=cv2.imread(image_path+"lancer.png")
saber_gold=cv2.imread(image_path+"saber_gold.png")

res = cv2.matchTemplate(img, atk_btn, cv2.TM_CCOEFF)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
top_left = max_loc

cv2.circle(img, top_left, 10, (0, 0, 0), lineType=2)

res = cv2.matchTemplate(img, quick, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = numpy.where(res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img, pt, (pt[0] + 50, pt[1] + 60), (0, 0, 0), 2)

res = cv2.matchTemplate(img, lancer, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = numpy.where(res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img, pt, (pt[0] + 50, pt[1] + 60), (0, 0, 0), 2)


img_small = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
cv2.imshow("H", img_small)

# pyautogui.moveTo(1, 1)

cv2.waitKey()
