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

from Config import config_manager, LanguageSetting

from LanguageWidget import LanguageWidget
from ShapeWidget import ShapeWidget
from InputWidget import InputWidget
from CandidateWidget import CandidateWidget
from JsonToBin import BinFileToJson


class KeyboardManager(QObject):
    _key_signal = Signal(str, list)

    mapping = {
        "comma": ",",
        "dot": ".",
        "leftbracket": "[",
        "rightbracket": "]",
        "quote": "'",
    }
    digit_mapping = {
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

        self._mapping = BinFileToJson("liu.bin")
        self._buffer = ""
        self._key = None
        if callback:
            self._key_signal.connect(callback)

    def _post_word(self, buf):
        self._buffer = buf
        result = self._mapping.get(buf, [])
        self._key_signal.emit(buf, result)

    def _output_word(self, buf, num):
        result = self._mapping.get(buf, [])
        if result:
            self._controller.type(result[num - 1])
        self._post_word("")

    def keyboard_event_handler(self, msg_ptr):
        message = msg_ptr.decode("utf-8")
        if message == "Ctrl+Space":
            self._key_signal.emit("SWITCH", [])
        
        logging.info(f"{config_manager.Language()}")
        comma_value = self.mapping.get(message, None)
        digit_value = self.digit_mapping.get(message, None)        
        if config_manager.Language() == LanguageSetting.ENGLISH:
            if len(message) == 1:
                self._controller.tap(message)
            elif comma_value:
                self._controller.tap(comma_value)
            elif digit_value:
                self._controller.tap(digit_value)
        elif message == "ESC":  # 清空候選區
            self._post_word("")
        elif message == "BACKSPACE":  # 候選區有值，調整候選區，沒值則執行倒退
            if self._buffer:
                self._post_word(self._buffer[:-1])
            else:
                self._controller.tap(keyboard.Key.backspace)
        elif message == "SPACE":  # 輸出候選區的第一個數值
            self._output_word(self._buffer, 1)
        elif digit_value: # 有數字的話，就是選項
            num = int(digit_value)
            if self._buffer:
                self._output_word(self._buffer, num)
            else:
                self._post_word("")
        elif comma_value:
            self._post_word(self._buffer + comma_value)
        elif message.isalpha():
            self._post_word(self._buffer + message)


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
