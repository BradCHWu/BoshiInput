import logging
import string

from pynput import keyboard

from PySide6.QtCore import QThread, Signal

from JsonToBin import BinFileToJson


class KeyboardManager(QThread):
    _key_signal = Signal(str, list)

    def __init__(self, callback):
        super().__init__()
        self._valid_key = list(string.ascii_letters)
        self._valid_key.extend(list(",.'[]"))
        self._report_key = list(string.digits)

        self._mapping = BinFileToJson("liu.bin")

        self._buffer = ""
        self._key = None
        self._modifier = {
            keyboard.Key.ctrl: False,
            keyboard.Key.alt: False,
            keyboard.Key.shift: False,
            keyboard.Key.cmd: False,
        }
        self._controller = keyboard.Controller()
        if callback:
            self._key_signal.connect(callback)




    def _has_modifier(self, key, pressed):
        mapping = {
            keyboard.Key.ctrl: keyboard.Key.ctrl,
            keyboard.Key.ctrl_l: keyboard.Key.ctrl,
            keyboard.Key.ctrl_r: keyboard.Key.ctrl,
            keyboard.Key.alt: keyboard.Key.alt,
            keyboard.Key.alt_l: keyboard.Key.alt,
            keyboard.Key.alt_r: keyboard.Key.alt,
            keyboard.Key.shift: keyboard.Key.shift,
            keyboard.Key.shift_l: keyboard.Key.shift,
            keyboard.Key.shift_r: keyboard.Key.shift,
            keyboard.Key.cmd: keyboard.Key.cmd,
            keyboard.Key.cmd_l: keyboard.Key.cmd,
            keyboard.Key.cmd_r: keyboard.Key.cmd,
        }
        ret = mapping.get(key, None)
        if ret is not None:
            self._modifier[ret] = pressed

    def _process_keys(self):
        active_mods = [mod for mod, active in self._modifier.items() if active]
       
        for mod in active_mods:
            self._controller.press(mod)
        try:
            self._controller.press(self._key)
            self._controller.release(self._key)
        except Exception as e:
            logging.error(f"Send taret {self._key} failed: {e}")

        for mod in active_mods:
            self._controller.release(mod)
        return True

    def on_press(self, _key):
        self._key = _key
        ret = False
        self._has_modifier(_key, True)

        if any(self._modifier.values()):
            logging.debug(f"Specific key {_key} pressed, exit...")
            return ret

        try:
            if hasattr(_key, "char") and _key.char in self._valid_key:
                key = _key.char
            else:
                key = None
            if key:
                self._buffer += key
                self._query_word()
                ret = True
        except AttributeError:
            ret = False
        return ret

    def on_release(self, key):
        self._has_modifier(key, False)

    def run(self):
        while True:
            self._keyboard_listener()

            key_ = self._key
            if not self._buffer:
                self._process_keys()
            elif key_ == keyboard.Key.space:
                logging.debug("Detect space")
                self._report_word(1)
            elif key_ == keyboard.Key.backspace:
                if self._buffer:
                    self._buffer = self._buffer[:-1]
                    self._query_word()
                else:
                    self._controller.tap(keyboard.Key.backspace)
            elif hasattr(key_, "char") and key_.char in self._report_key:
                key = key_.char
                num = int(key)
                self._report_word(num)

    def _keyboard_listener(self):
        press = self.on_press
        release = self.on_release
        with keyboard.Listener(press, release, suppress=True) as listen:
            listen.join()

    def _query_word(self):
        result = self._mapping.get(self._buffer, [])
        self._key_signal.emit(self._buffer, result)

    def _report_word(self, num: int):
        result = self._mapping.get(self._buffer, [])
        if result:
            if num <= len(result):
                self._controller.type(result[num - 1])
            else:
                logging.info(f"message: {num}")
                self._controller.type(f"{num}")
        self._buffer = ""
        self._key_signal.emit(self._buffer, [])
