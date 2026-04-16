from pynput import keyboard


class KeyboardMove:
    def __init__(self):
        self.keyboardController = keyboard.Controller()

    def Type(self, message):
        self.keyboardController.tap(message)

    def TapSpace(self):
        self.keyboardController.tap(keyboard.Key.space)

    def TapBackspace(self):
        self.keyboardController.tap(keyboard.Key.backspace)
