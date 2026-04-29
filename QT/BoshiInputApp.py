from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSharedMemory

from QT.MainFrame import MainFrame
from QT.setting import Name


class BoshiInputApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.checker = QSharedMemory(Name())
        if self.checker.attach():
            raise Exception("程式正在執行中")

        if not self.checker.create(1):
            raise Exception("無法建立共享記憶體，可能是程式正在執行中或系統資源不足")

        self.frame = MainFrame()
        self.frame.show()
        self.setQuitOnLastWindowClosed(False)
