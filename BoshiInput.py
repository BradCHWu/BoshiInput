import sys

from PySide6.QtWidgets import QApplication

from MainFrame import MainFrame

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = MainFrame()
    window.show()
    sys.exit(app.exec())
