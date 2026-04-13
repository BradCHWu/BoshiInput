import logging
import ctypes
import os

from PySide6.QtWidgets import (
    QSplitter,
    QHBoxLayout,
    QWidget,
)
from PySide6.QtCore import Qt, QObject, Signal
from pynput import keyboard

from Config import config_manager

from LanguageWidget import LanguageWidget
from ShapeWidget import ShapeWidget
from InputWidget import InputWidget
from CandidateWidget import CandidateWidget
from JsonToBin import BinFileToJson

class KeyboardManager(QObject):
    _key_signal = Signal(str, list)
    def __init__(self, callback):
        super().__init__()

        dll_path = os.path.abspath("./keyboard.dll")        
        try:
            kbd_lib = ctypes.CDLL(dll_path)
        except OSError as e:
            logging.error(f"Failed to load keyboard.dll from {dll_path}: {e}")
        CALLBACK_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p)
        self.c_callback = CALLBACK_FUNC(self.keyboard_event_handler)
        kbd_lib.start_keyboard_hook(self.c_callback)
        self._controller = keyboard.Controller()

        self._mapping  = BinFileToJson("liu.bin")
        self._buffer = ""
        self._key = None
        if callback:
            self._key_signal.connect(callback)

    def keyboard_event_handler(self, msg_ptr):
        message = msg_ptr.decode('utf-8')
        
        if message == "CTRL_SPACE":
            logging.info("\n[系統] 偵測到 Ctrl + Space！")
        elif message == "ESC":
            self._buffer = ""
            self._key_signal.emit("", [])
        elif message == "BACKSPACE":
            if self._buffer:
                self._buffer = self._buffer[:-1]
                self._key_signal.emit("", self._mapping.get(self._buffer, []))
            else:
                self._controller.tap(keyboard.Key.backspace)
        elif message == "SPACE":
            result = self._mapping.get(self._buffer, [])
            self._key_signal.emit("", result[0])
            self._controller.type(result[0])
            logging.info(f"Get word {result[0]}")
            self._buffer = ""
        elif len(message) == 1:
            self._buffer += message
            self._key_signal.emit(message, self._mapping.get(self._buffer, []))



class BoshiInputView(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self._keyboard_manager = KeyboardManager(self._handle_keypress)

        self._languageWidget = LanguageWidget()
        self._shapeWidget = ShapeWidget()
        self._inputWidget = InputWidget()
        self._candidateWidget = CandidateWidget()

        style_sheet = """
        QSplitter::handle {
                background-color: #cccccc;
            }
        """

        self._splitter = QSplitter(Qt.Orientation.Horizontal)
        self._splitter.setHandleWidth(2)
        self._splitter.setStyleSheet(style_sheet)
        self._splitter.addWidget(self._languageWidget)
        self._splitter.addWidget(self._shapeWidget)
        self._splitter.addWidget(self._inputWidget)
        self._splitter.addWidget(self._candidateWidget)
        size = [30, 30, 60, 200]
        self._splitter.setSizes(size)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._splitter)

        height = max(10, self.height() * 0.7)
        for i in range(self._splitter.count()):
            w = self._splitter.widget(i)
            w.UpdateFont(height)
            width = w.WidthWithChar()
            logging.debug(f"Width = {width}")
            w.setFixedWidth(width)

    def _handle_keypress(self, key, keyList):
        if key == "SWITCH":
            config_manager.NextLanguage()
            self._splitter.widget(0).ShowLanguage()
        else:
            self._splitter.widget(2).Send(key)
            self._splitter.widget(3).Send(keyList)


