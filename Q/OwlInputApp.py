from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QSharedMemory

from Q.MainFrame import MainFrame
from Q.setting import Name


class OwlInputApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.status = True
        try:
            self.checker = QSharedMemory(Name())
            if self.checker.attach():
                raise Exception("程式正在執行中")

            if not self.checker.create(1):
                raise Exception("無法建立共享記憶體")
        except Exception as e:
            QMessageBox.warning(None, "提示", str(e))
            self.status = False

        if not self.status:
            return

        self.frame = MainFrame()
        self.frame.show()
        self.setQuitOnLastWindowClosed(False)
