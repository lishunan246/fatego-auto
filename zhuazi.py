# coding=utf-8

from Screen import Screen
import time
import threading


class Zhuazi(threading.Thread):
    def __init__(self, parent, fresh_start=True):
        super().__init__()
        self.fresh_start = fresh_start
        self.parent = parent
        self._stop = threading.Event()
        self.cnt = 0
        self.parent.status_changed()
        self.screen = Screen(parent)
        self.do_loop = True

    def stop(self):
        self._stop.set()
        self.screen.stop()

    def stopped(self):
        return self._stop.is_set()

    def quit_on_complete(self):
        self.do_loop = False

    def run(self):
        self.parent.status_changed()
        screen = self.screen
        while self.do_loop:
            start_time = time.time()
            if self.fresh_start:
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

            else:
                self.fresh_start = True

            # attack
            # 选3张卡 循环

            while not screen.have('jiban'):
                if self.stopped():
                    return

                if screen.have('atk_btn'):
                    screen.fight()
                elif screen.have('network_error'):
                    screen.click_on('retry')
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
            self.cnt += 1
            self.parent.status_changed()
            self.parent.add_text("---战斗 %s 完成 历时 %s 秒 ---" % (self.cnt, time.time() - start_time))
