# coding=utf-8

from Screen import Screen
import time

cnt = 0
screen = Screen()
while True:
    start_time = time.time()
    # 点击黑森林
    target = 'target'
    screen.click_on(target, repeat=True, loader=screen.target)
    if screen.have('huangjinguoshi'):
        screen.click_on('huangjinguoshi')
        screen.click_on('jueding')
        screen.click_on(target, loader=screen.target)

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

    if screen.have('lvup'):
        screen.click_on('lvup', repeat=True)

    if screen.have('jibanup'):
        screen.click_on('jibanup', repeat=True)

    # 点击exp
    screen.click_on('exp', repeat=True)

    if screen.have('lvup'):
        screen.click_on('lvup', repeat=True)

    screen.click_on('xiayibu')
    cnt += 1
    print("---战斗 %s 完成 历时 %s 秒 ---" % (cnt, time.time() - start_time))
