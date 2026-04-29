import sys

from PySide6.QtWidgets import QMessageBox
from QT.BoshiInputApp import BoshiInputApp


if __name__ == "__main__":
    try:
        app = BoshiInputApp(sys.argv)
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.warning(None, "提示", str(e))
        sys.exit(0)
