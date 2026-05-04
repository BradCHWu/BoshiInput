import logging


from PySide6.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu, QApplication
from PySide6.QtCore import Qt, QPoint, QRect, QSize
from PySide6.QtGui import QAction

from setting import LoadPNG, png_Owl, Name
from Q.OwlInputView import OwlInputView

from Config import config_manager


class MainFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        config_manager.InstallCallback(self._input_callback)

        window_style = Qt.WindowType.FramelessWindowHint
        window_style |= Qt.WindowType.Tool
        window_style |= Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(window_style)
        self.setWindowIcon(LoadPNG(png_Owl))

        self._view = OwlInputView(self)
        self.setCentralWidget(self._view)

        self._restorePosition()
        self._create_tray_icon()
        logging.info(f"Application {Name()} initialize")

    def _input_callback(self, in_char, candidates):
        logging.debug(f"Input: {in_char}, Candidates: {candidates}")
        self._view.Update(in_char, candidates)

    def _restorePosition(self):
        p = config_manager.GetPosition()
        pos = QPoint(*p)
        sz = QSize(30, 30)
        self.setGeometry(QRect(pos, sz))

    def _create_tray_icon(self):
        self._tray = QSystemTrayIcon(LoadPNG(png_Owl), self)

        menu = QMenu()
        exit_action = QAction("Close", self)
        exit_action.triggered.connect(QApplication.instance().quit)
        menu.addAction(exit_action)
        self._tray.setContextMenu(menu)
        self._tray.show()

    def closeEvent(self, event):
        config_manager.Save()
        logging.info(f"Application {Name()} closed")
        return super().closeEvent(event)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            gp = event.globalPosition().toPoint()
            topLeft = self.frameGeometry().topLeft()
            self._drag_position = gp - topLeft
        if event.buttons() == Qt.MouseButton.RightButton:
            self._tray.contextMenu().popup(event.globalPosition().toPoint())

        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            gp = event.globalPosition().toPoint()
            self.move(gp - self._drag_position)
            pt = self.geometry().topLeft()
            config_manager.SetPosition((pt.x(), pt.y()))

        return super().mouseMoveEvent(event)
