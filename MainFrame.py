from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt, QPoint, QRect, QSize

from setting import LoadPNG, png_Boshi
from Config import Config
from CommonTool import fromQPoint, toQPoint


class MainFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowIcon(LoadPNG(png_Boshi))

        self._config = Config()

        self._restorePosition()

    def _restorePosition(self):
        self._drag_position = QPoint()

        str_pos = self._config.Position()
        p = toQPoint(str_pos)
        sz = QSize(200, 50)
        self.setGeometry(QRect(p, sz))

    def closeEvent(self, event):
        self._config.Save()
        return super().closeEvent(event)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            gp = event.globalPosition().toPoint()
            topLeft = self.frameGeometry().topLeft()
            self._drag_position = gp - topLeft

        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            gp = event.globalPosition().toPoint()
            self.move(gp - self._drag_position)
            self._config.SetPosition(fromQPoint(self.geometry().topLeft()))

        return super().mouseMoveEvent(event)
