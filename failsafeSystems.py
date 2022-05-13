import os
import sys

from PyQt6.QtWidgets import QApplication

from core import Core
from report import Report
from settings import Settings


def main():
    check_file_settings = os.path.exists('settings.yaml')
    settings = Settings()
    report = Report()
    app = QApplication(sys.argv)
    if check_file_settings is True:
        settings.read_settings('settings.yaml')
    else:
        settings.create_settings('settings.yaml')
    core = Core(settings, report)
    core.window_show()

    app.exec()


if __name__ == '__main__':
    main()
