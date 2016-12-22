# coding=utf-8

import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

def main():
    print("init")

    sys._excepthook = sys.excepthook
    sys.excepthook = my_exception_hook

    app = QApplication(sys.argv)
    win = MainWindow()

    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")

if __name__ == '__main__':
    main()


