import logging
import string

from pynput import keyboard

from PySide6.QtCore import QThread, Signal

from JsonToBin import BinFileToJson


class KeyboardManager(QThread):
    key_signal = Signal(list)

    def __init__(self, callback):
        super().__init__()
        self._valid_key = list(string.ascii_letters)
        self._valid_key.extend([',', '.'])
        self.mapping = BinFileToJson("liu.bin")
        self.buffer = ""
        self.key = None
        self._controller = keyboard.Controller()
        if callback:
            self.key_signal.connect(callback)

    def on_press(self, key):
        self.key = key
        if hasattr(key, "char") and key.char in self._valid_key:
            self.buffer += key.char
            result = self.mapping.get(self.buffer, [])
            self.key_signal.emit(result)
            return True
        return False 

    def run(self):
        while True:
            with keyboard.Listener(on_press=self.on_press, suppress=True) as listen:
                listen.join()
           
            if self.key == keyboard.Key.space:
                result = self.mapping.get(self.buffer, [])
                if result:
                    self._controller.type(result[0])
                else:
                    self._controller.tap(keyboard.Key.space)
                self.buffer = ""
                self.key_signal.emit([])

            elif hasattr(self.key, "char") and self.key.char in string.digits:
                result = self.mapping.get(self.buffer, [])
                num = int(self.key.char)
                if self.buffer and num <= len(result):
                    self._controller.type(result[num - 1])
                    self.buffer = ""
                    self.key_signal.emit([])
                else:
                    self._controller.tap(self.key)

            elif self.key == keyboard.Key.backspace:
                if self.buffer:
                    self.buffer = self.buffer[:-1]
                    result = self.mapping.get(self.buffer, [])
                    self.key_signal.emit(result)
                else:
                    self._controller.tap(keyboard.Key.backspace)

            else:
                if self.key is not None:
                    self._controller.press(self.key)
                    self._controller.release(self.key)