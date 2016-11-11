# coding=utf-8

from Screen import Screen
import time

screen = Screen()
while True:
    start_time = time.time()
    # 点击黑森林
    screen.click_on('heisenlin')

    # 助战选择 第一个？
    screen.click_on('zhuzhan')

    # 开始任务
    screen.click_on('kaishirenwu')

    # attack
    # 选3张卡 循环

    while not screen.have('jiban'):
        if screen.have('atk_btn'):
            screen.fight()
        else:
            time.sleep(0.5)

    # 点击 羁绊
    screen.click_on('jiban', repeat=True)

    # 点击exp
    screen.click_on('exp', repeat=True)

    screen.click_on('xiayibu')

    print "---战斗完成 历时 %s 秒 ---" % (time.time() - start_time)
