from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QSharedMemory

from QT.MainFrame import MainFrame
from QT.setting import Name


class BoshiInputApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.status = None
        self.checker = QSharedMemory(Name())
        if self.checker.attach():
            QMessageBox.warning(None, "提示", "程式正在執行中")
            self.status = "running"

        if not self.checker.create(1):
            QMessageBox.warning(None, "提示", "無法建立共享記憶體")
            self.status = "error"

        if self.status is None:
            self.frame = MainFrame()
            self.frame.show()
            self.setQuitOnLastWindowClosed(False)
