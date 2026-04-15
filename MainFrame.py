import logging

from PySide6.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu, QApplication
from PySide6.QtCore import Qt, QPoint, QRect, QSize
from PySide6.QtGui import QAction

from setting import LoadPNG, png_Boshi, Name
from Config import config_manager, LanguageSetting
from CommonTool import fromQPoint, toQPoint
from KeyboardInputHandler import KeyboardInputHandler
from BoshiInputView import BoshiInputView


class MainFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self._window_style())
        self.setWindowIcon(LoadPNG(png_Boshi))

        self._initial_logging()

        self._keyboard_manager = KeyboardInputHandler(self._handle_keypress)

        self._view = BoshiInputView(self)
        self.setCentralWidget(self._view)

        self._restorePosition()
        self._create_tray_icon()
        logging.info(f"Application {Name()} initialize")

    def _window_style(self):
        window_style = Qt.WindowType.FramelessWindowHint
        window_style |= Qt.WindowType.Tool
        window_style |= Qt.WindowType.WindowStaysOnTopHint
        return window_style

    def _initial_logging(self):
        logging_file = None
        if config_manager.LoggingFile():
            logging_file = f"{Name()}.log"
        logging_level = config_manager.LoggingLevel()
        logging_format = "[%(levelname)s] %(lineno)s %(message)s"
        logging.basicConfig(
            filename=logging_file,
            filemode="a",
            level=logging_level,
            format=logging_format,
        )

    def _restorePosition(self):
        self._drag_position = QPoint()

        str_pos = config_manager.Position()
        p = toQPoint(str_pos)
        # sz = QSize(200, 50)
        sz = QSize(50, 50)
        self.setGeometry(QRect(p, sz))

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

    def _handle_keypress(self, key, keyList):
        if key == "SWITCH":
            config_manager.NextLanguage()
            self._view.ShowLanguage()
            self._hide(self._hide_action.isChecked())
            logging.info(f"{config_manager.Language()}")
        else:
            self._view.Send(key, keyList)

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
            config_manager.SetPosition(fromQPoint(self.geometry().topLeft()))
            logging.debug(f"Move {Name()} to {config_manager.Position()}")

        return super().mouseMoveEvent(event)
