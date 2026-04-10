import keyboard
import pyperclip

from PySide6.QtCore import QThread, Signal

from JsonToBin import BinFileToJson


class KeyboardManager(QThread):
    key_signal = Signal(list)

    def __init__(self, callback):
        super().__init__()
        self.mapping = BinFileToJson("liu.bin")
        self.buffer = ""

        if callback:
            self.key_signal.connect(callback)

    def send_value(self, key):
        pyperclip.copy(key)
        keyboard.send("ctrl+v")

    def send_clear(self):
        self.buffer = ""
        self.key_signal.emit([])

    def on_key_event(self, event):
        if event.event_type == "up":
            return False

        name = event.name
        if len(name) == 1:
            if name.isalpha():
                self.buffer += name
                result = self.mapping.get(self.buffer, [])
                self.key_signal.emit(result)
            elif name.isdigit():
                result = self.mapping.get(self.buffer, [])
                num = int(name)
                if num <= len(result):
                    self.send_value(result[num - 1])
                self.send_clear()

            return False
        elif name == "space":
            if not self.buffer:
                return True
            result = self.mapping.get(self.buffer, [])
            if result:
                self.send_value(result[0])
            self.send_clear()
            return False if result else True
        return True

    def run(self):
        keyboard.hook(self.on_key_event, suppress=True)
        keyboard.wait()
