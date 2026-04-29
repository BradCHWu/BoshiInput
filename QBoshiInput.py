import sys

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QSharedMemory

from QT.MainFrame import MainFrame
from QT.setting import Name

if __name__ == "__main__":
    app = QApplication(sys.argv)

    shared_memory = QSharedMemory(Name())
    if shared_memory.attach():
        QMessageBox.warning(None, "提示", "程式正在執行中")
        sys.exit(0)

    if not shared_memory.create(1):
        QMessageBox.warning(None, "提示", "無法建立共享記憶體")
        sys.exit(0)

    app.setQuitOnLastWindowClosed(False)
    window = MainFrame()
    window.show()
    sys.exit(app.exec())
