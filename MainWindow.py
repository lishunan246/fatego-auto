# coding=utf-8

from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QTextBrowser
from PyQt5.QtGui import QIcon
from zhuazi import Zhuazi


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.zhuazi = None
        self.statusBar().showMessage('ready')
        self.resize(250, 150)
        self.move(300, 300)
        self.setWindowTitle('刷起来')
        self.setWindowIcon(QIcon('icon.ico'))

        self.toolBar = self.addToolBar('')

        loop_action = QAction(QIcon('./image/ui/loop.png'), 'Loop', self)
        loop_action.triggered.connect(self.start_loop)

        continue_action = QAction(QIcon('./image/ui/continue.png'), 'Continue', self)
        continue_action.triggered.connect(self.continue_loop)

        exit_action = QAction(QIcon('./image/ui/exit.png'), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.stop_loop)

        self.toolBar.addAction(loop_action)
        self.toolBar.addAction(continue_action)
        self.toolBar.addAction(exit_action)

        txt = QTextBrowser()
        txt.setContentsMargins(5, 5, 5, 5)
        self.setCentralWidget(txt)
        self.show()

    def add_text(self, text):
        self.centralWidget().append(text)
        sb = self.centralWidget().verticalScrollBar()
        sb.setValue(sb.maximum())
        print(text)

    def closeEvent(self, *args, **kwargs):
        self.stop_loop()
        print("关闭程序")

    def status_changed(self):
        if self.zhuazi is None:
            self.statusBar().showMessage("就绪。")
        elif self.zhuazi.stopped():
            self.statusBar().showMessage("已停止。")
        else:
            self.statusBar().showMessage("当前次数： " + str(self.zhuazi.cnt))

    def start_loop(self):
        if self.zhuazi is not None and not self.zhuazi.stopped():
            return

        self.zhuazi = Zhuazi(self, fresh_start=True)
        self.zhuazi.start()

    def continue_loop(self):
        if self.zhuazi is not None and not self.zhuazi.stopped():
            return

        self.zhuazi = Zhuazi(self, fresh_start=False)
        self.zhuazi.start()

    def stop_loop(self):
        if self.zhuazi is None:
            return
        self.zhuazi.stop()
