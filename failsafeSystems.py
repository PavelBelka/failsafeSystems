import sys

from core import Core
from PyQt6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    presenter = Core(None)
    presenter.window_show()
    app.exec()

if __name__ == '__main__':
    main()