from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt, QPoint

from setting import LoadPNG, png_Boshi


class MainFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowIcon(LoadPNG(png_Boshi))

        self._drag_position = None

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

        return super().mouseMoveEvent(event)
