import logging

from PySide6.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu, QApplication
from PySide6.QtCore import Qt, QPoint, QRect, QSize
from PySide6.QtGui import QAction

from setting import LoadPNG, png_Boshi
from Config import config_manager
from CommonTool import fromQPoint, toQPoint
from BoshiInputView import BoshiInputView


class MainFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self._window_style())
        self.setWindowIcon(LoadPNG(png_Boshi))

        self._initial_logging()

        self._view = BoshiInputView(self)
        self.setCentralWidget(self._view)

        self._restorePosition()
        self._create_tray_icon()

    def _window_style(self):
        window_style = Qt.WindowType.FramelessWindowHint
        window_style |= Qt.WindowType.Tool
        window_style |= Qt.WindowType.WindowStaysOnTopHint
        return window_style

    def _initial_logging(self):
        logging_level = config_manager.LoggingLevel()
        logging_format = "[%(levelname)s] %(lineno)s %(message)s"
        logging.basicConfig(level=logging_level, format=logging_format)

    def _restorePosition(self):
        self._drag_position = QPoint()

        str_pos = config_manager.Position()
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
        config_manager.Save()
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
            config_manager.SetPosition(fromQPoint(self.geometry().topLeft()))

        return super().mouseMoveEvent(event)
