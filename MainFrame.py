import logging

from PySide6.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu, QApplication
from PySide6.QtCore import Qt, QPoint, QRect, QSize
from PySide6.QtGui import QAction

from setting import LoadPNG, png_Boshi
from Config import Config
from CommonTool import fromQPoint, toQPoint
from BoshiInputView import BoshiInputView


class MainFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        window_style = Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool
        self.setWindowFlags(window_style)
        self.setWindowIcon(LoadPNG(png_Boshi))

        self._config = Config()
        self._initial_logging()

        self._view = BoshiInputView(self)
        self.setCentralWidget(self._view)

        self._restorePosition()
        self._create_tray_icon()

    def _initial_logging(self):
        logging_level = self._config.LoggingLevel()
        logging_format = "[%(levelname)s] %(lineno)s %(message)s"
        logging.basicConfig(level=logging_level, format=logging_format)

    def _restorePosition(self):
        self._drag_position = QPoint()

        str_pos = self._config.Position()
        p = toQPoint(str_pos)
        sz = QSize(200, 50)
        self.setGeometry(QRect(p, sz))

    def _create_tray_icon(self):
        self._tray = QSystemTrayIcon(LoadPNG(png_Boshi), self)

        menu = QMenu()
        exit_action = QAction("關閉", self)
        exit_action.triggered.connect(QApplication.instance().quit)
        menu.addAction(exit_action)
        self._tray.setContextMenu(menu)
        self._tray.show()

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
