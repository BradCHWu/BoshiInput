import os
import ctypes
import logging

from pynput import keyboard

from PySide6.QtCore import QObject, Signal

from Config import config_manager
from FileConvert import BinFileToJson


class KeyboardInputHandler(QObject):
    HOOK_LIBRARY_PATH = "./keyboard.dll" if os.name == "nt" else "./keyboard.so"
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

    def __init__(self, callback):
        super().__init__()

        if os.path.exists(self.HOOK_LIBRARY_PATH):
            dll_path = os.path.abspath(self.HOOK_LIBRARY_PATH)
            try:
                kbd_lib = ctypes.CDLL(dll_path)
            except OSError as e:
                logging.error(f"Failed to load {self.HOOK_LIBRARY_PATH}: {e}")
        else:
            dll_path = None
            logging.error(f"{self.HOOK_LIBRARY_PATH} not found")

        CALLBACK_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p)
        self.c_callback = CALLBACK_FUNC(self.handleKeyboardEvent)
        kbd_lib.start_keyboard_hook(self.c_callback)
        self.keyboardController = keyboard.Controller()

        if os.path.exists(self.DEFAULT_MAPPING_FILE):
            self.wordMapping = BinFileToJson("liu.bin")
        else:
            self.wordMapping = None
            logging.error(f"{self.DEFAULT_MAPPING_FILE} not found")
        self.inputBuffer = ""
        self.lastKeyPressed = None
        if callback:
            self.wordCandidateSignal.connect(callback)

    def updateCandidates(self, buf):
        self.inputBuffer = buf
        result = self.wordMapping.get(buf, [])
        self.wordCandidateSignal.emit(buf, result)

    def commitCandidate(self, buf, num):
        result = self.wordMapping.get(buf, [])
        if result and num < len(result):
            self.keyboardController.type(result[num])
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
        if message == "ESC":
            self.updateCandidates("")
        elif message == "BACKSPACE":  # 候選區有值，調整候選區，沒值則執行倒退
            if is_english or not self.inputBuffer:
                self.keyboardController.tap(keyboard.Key.backspace)
            elif self.inputBuffer:
                self.updateCandidates(self.inputBuffer[:-1])
        elif message == "SPACE":  # 輸出候選區的第一個數值
            if is_english or not self.inputBuffer:
                self.keyboardController.tap(keyboard.Key.space)
            else:
                self.commitCandidate(self.inputBuffer, 0)
        elif digit_value:  # 有數字的話，就是選項
            num = int(digit_value)
            if is_english or not self.inputBuffer:
                self.keyboardController.tap(digit_value)
                self.updateCandidates("")
            else:
                self.commitCandidate(self.inputBuffer, num)
        elif comma_value:
            if is_english:
                self.keyboardController.tap(comma_value)
            else:
                self.updateCandidates(self.inputBuffer + comma_value)
        elif message.isalpha():
            if is_english:
                self.keyboardController.tap(message)
            else:
                self.updateCandidates(self.inputBuffer + message)
