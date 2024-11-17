import sys
import os
from MainWindow import MainWindow
from PyQt6.QtWidgets import QApplication


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    application = QApplication(sys.argv)

    windowClass = MainWindow()
    windowClass.show()


    sys.excepthook = except_hook

    sys.exit(application.exec())
