# coding=utf-8

import threading
import time

from GameStatus import *
from Screen import Screen


class Zhuazi(threading.Thread):
    def __init__(self):
        super().__init__()

        self._stop = threading.Event()
        self.cnt = 0
        GameStatus().window.status_changed()
        self.screen = Screen()
        self.do_loop = True

    def stop(self):
        self._stop.set()
        self.screen.stop()

    def stopped(self):
        return self._stop.is_set()

    def quit_on_complete(self):
        self.do_loop = False

    def fight(self):
        GameStatus().current_level = Screen().get_current_level()
        if GameStatus().current_level == 3:
            for key in Screen()._skills.get_all():
                while Screen().have(key, loader=Screen()._skills):
                    if Screen()._stop:
                        return
                    Screen().click_on(key, loader=Screen()._skills)
                    time.sleep(2)
                    Screen().log('use ' + key)

        GameStatus().cards = []

        while len(GameStatus().cards) < 3:
            if self._stop:
                return

            if Screen().have('atk_btn'):
                Screen().click_on('atk_btn')
                time.sleep(1)

                Screen().get_cards()

        for i in range(0, 3):
            x, y = GameStatus().cards[i]
            Screen()._click(x, y)
            time.sleep(Screen()._delay)

    def run(self):
        GameStatus().window.status_changed()
        screen = self.screen
        while self.do_loop:

            start_time = time.time()
            if GameStatus().game_stage == GameStage.BeforeFight:
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

                GameStatus().game_stage = GameStage.Fighting

            elif GameStatus().game_stage == GameStage.Fighting:
                # attack
                # 选3张卡 循环

                while not screen.have('jiban'):
                    if self.stopped():
                        return

                    if screen.have('atk_btn'):
                        self.fight()
                    elif screen.have('network_error'):
                        screen.click_on('retry')
                    else:
                        time.sleep(0.5)

                        GameStatus().game_stage = GameStage.AfterFight

            else:

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
                self.cnt += 1
                GameStatus().window.status_changed()
                GameStatus().window.add_text("---战斗 %s 完成 历时 %s 秒 ---" % (self.cnt, time.time() - start_time))
                GameStatus().game_stage = GameStage.BeforeFight
