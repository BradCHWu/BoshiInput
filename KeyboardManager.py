from pynput import keyboard
from PySide6.QtCore import QThread, Signal

from JsonToBin import BinFileToJson

class KeyboardManager(QThread):
    key_signal = Signal(bool, list)

    def __init__(self, callback):
        super().__init__()

        self.mapping = BinFileToJson("liu.bin")
        self.key = ""
        self.key_signal.connect(callback)


    def on_press(self, key):
        send_done = False
        try:
            k = key.char
        except:
            k = None
            if key == keyboard.Key.space:
                send_done = True

        if k is not None:
            self.key += k
        
        result = self.mapping.get(self.key)
        self.key_signal.emit(send_done, result)

    def run(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()
