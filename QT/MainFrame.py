import logging


from PySide6.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu, QApplication
from PySide6.QtCore import Qt, QPoint, QRect, QSize
from PySide6.QtGui import QAction

from QT.setting import LoadPNG, png_Boshi, Name
from QT.CommonTool import fromQPoint, toQPoint
from QT.BoshiInputView import BoshiInputView

from Config import config_manager, LanguageSetting
from BoshiCore import BoshiCore


class MainFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        BoshiCore(self._input_callback)

        window_style = Qt.WindowType.FramelessWindowHint
        window_style |= Qt.WindowType.Tool
        window_style |= Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(window_style)
        self.setWindowIcon(LoadPNG(png_Boshi))

        self._view = BoshiInputView(self)
        self.setCentralWidget(self._view)

        self._restorePosition()
        self._create_tray_icon()
        logging.info(f"Application {Name()} initialize")

    def _input_callback(self, in_char, candidates):
        logging.debug(f"Input: {in_char}, Candidates: {candidates}")
        # self._view.Update(in_char, candidates)

    def _restorePosition(self):
        p = config_manager.GetPosition()
        pos = QPoint(*p)
        sz = QSize(50, 50)
        self.setGeometry(QRect(pos, sz))

    def _create_tray_icon(self):
        self._tray = QSystemTrayIcon(LoadPNG(png_Boshi), self)

        menu = QMenu()
        self._hide_action = QAction("Hide", self)
        self._hide_action.setCheckable(True)
        self._hide_action.setChecked(True)
        self._hide_action.toggled.connect(self._hide)
        exit_action = QAction("Close", self)
        exit_action.triggered.connect(QApplication.instance().quit)
        menu.addAction(self._hide_action)
        menu.addAction(exit_action)
        self._tray.setContextMenu(menu)
        self._tray.show()

    def _hide(self, checked):
        if checked:
            if config_manager.Language() == LanguageSetting.ENGLISH:
                self.hide()
            else:
                self.show()
        else:
            self.show()

    def closeEvent(self, event):
        config_manager.Save()
        logging.info(f"Application {Name()} closed")
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
            pt = self.geometry().topLeft()
            config_manager.SetPosition((pt.x(), pt.y()))

        return super().mouseMoveEvent(event)
