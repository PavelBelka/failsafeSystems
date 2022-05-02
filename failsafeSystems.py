import sys, os.path

from core import Core
from PyQt6.QtWidgets import QApplication
from settings import Settings

def main():
    check_file = os.path.exists('settings.yaml')
    settings = Settings()
    if check_file is True:
        settings.read_settings('settings.yaml')
    else:
        settings.create_settings('settings.yaml')
    app = QApplication(sys.argv)
    presenter = Core(None, settings)
    presenter.window_show()
    app.exec()

if __name__ == '__main__':
    main()