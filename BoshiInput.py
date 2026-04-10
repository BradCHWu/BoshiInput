import sys
import logging

from PySide6.QtWidgets import QApplication

from MainFrame import MainFrame

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = MainFrame()
    window.show()
    sys.exit(app.exec())
