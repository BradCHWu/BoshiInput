import logging
import os

from PySide6.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu, QApplication
from PySide6.QtCore import Qt, QPoint, QRect, QSize, Signal
from PySide6.QtGui import QAction

from QT.setting import LoadPNG, png_Boshi, Name
from QT.CommonTool import fromQPoint, toQPoint
from QT.BoshiInputView import BoshiInputView

from Config import config_manager, LanguageSetting
from FileConvert import BinFileToJson
from KeyboardGrab import KeyboardGrab
from KeyboardMove import KeyboardMove


class MainFrame(QMainWindow):
    HOOK_LIBRARY_PATH = "keyboard.dll" if os.name == "nt" else "keyboard.so"
    DEFAULT_MAPPING_FILE = "liu.bin"
    wordCandidateSignal = Signal(str, list)

    punctuationMapping = {
        "comma": ",",
        "dot": ".",
        "leftbracket": "[",
        "rightbracket": "]",
        "quote": "'",
    }
    digitKeyMapping = {
        "NUM0": "0",
        "NUM1": "1",
        "NUM2": "2",
        "NUM3": "3",
        "NUM4": "4",
        "NUM5": "5",
        "NUM6": "6",
        "NUM7": "7",
        "NUM8": "8",
        "NUM9": "9",
    }

    def __init__(self):
        super().__init__()
        self._initial_logging()

        self.setWindowFlags(self._window_style())
        self.setWindowIcon(LoadPNG(png_Boshi))

        cur_path = os.path.abspath(os.path.curdir)
        dll_file = os.path.join(cur_path, self.HOOK_LIBRARY_PATH)
        self.grab = KeyboardGrab.Hook(dll_file, self.handleKeyboardEvent)
        self.wordCandidateSignal.connect(self._handle_keypress)

        self.keyboard = KeyboardMove()

        bin_file = os.path.join(cur_path, self.DEFAULT_MAPPING_FILE)
        if os.path.exists(bin_file):
            self.wordMapping = BinFileToJson(bin_file)
        else:
            self.wordMapping = None
            logging.error(f"{bin_file} not found")

        self.inputBuffer = ""

        self._view = BoshiInputView(self)
        self.setCentralWidget(self._view)

        self._restorePosition()
        self._create_tray_icon()
        logging.info(f"Application {Name()} initialize")

    def updateCandidates(self, buf):
        self.inputBuffer = buf
        result = self.wordMapping.get(buf, [])
        self.wordCandidateSignal.emit(buf, result)

    def commitCandidate(self, buf, num):
        result = self.wordMapping.get(buf, [])
        if result and num < len(result):
            self.keyboard.Type(result[num])
        self.updateCandidates("")

    def handleKeyboardEvent(self, msg_ptr):
        message = msg_ptr.decode("utf-8")
        if message == "Ctrl+Space":
            self.updateCandidates("")
            self.wordCandidateSignal.emit("SWITCH", [])
            return

        is_english = config_manager.IsEnglish()

        comma_value = self.punctuationMapping.get(message, None)
        digit_value = self.digitKeyMapping.get(message, None)
        if len(message) == 1 and message.isalpha():
            if is_english:
                self.keyboard.Type(message)
            else:
                self.updateCandidates(self.inputBuffer + message)
        elif message == "SPACE":  # 輸出候選區的第一個數值
            if is_english or not self.inputBuffer:
                self.keyboard.TapSpace()
            else:
                self.commitCandidate(self.inputBuffer, 0)
        elif message == "BACKSPACE":  # 候選區有值，調整候選區，沒值則執行倒退
            if is_english or not self.inputBuffer:
                self.keyboard.TapBackspace()
            elif self.inputBuffer:
                self.updateCandidates(self.inputBuffer[:-1])
        elif digit_value:  # 有數字的話，就是選項
            if is_english or not self.inputBuffer:
                self.keyboard.Type(digit_value)
                self.updateCandidates("")
            else:
                num = int(digit_value)
                self.commitCandidate(self.inputBuffer, num)
        elif comma_value:
            if is_english:
                self.keyboard.Type(comma_value)
            else:
                self.updateCandidates(self.inputBuffer + comma_value)
        elif message == "ESC":
            self.updateCandidates("")

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
