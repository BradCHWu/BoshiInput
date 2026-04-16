import os
import ctypes
import logging


class KeyboardGrab:
    c_callback = None
    bind_library = None

    @staticmethod
    def Hook(dll_file, callback):
        if os.path.exists(dll_file):
            dll_path = os.path.abspath(dll_file)
            try:
                KeyboardGrab.bind_library = ctypes.CDLL(dll_path)
            except OSError as e:
                logging.error(f"Failed to load {dll_file}: {e}")
        else:
            dll_path = None
            logging.error(f"{dll_file} not found")

        CALLBACK_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p)
        KeyboardGrab.c_callback = CALLBACK_FUNC(callback)
        KeyboardGrab.bind_library.start_keyboard_hook(KeyboardGrab.c_callback)

    @staticmethod
    def Unhook():
        KeyboardGrab.bind_library.stop_keyboard_hook()
