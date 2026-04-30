import os
import logging

from KeyboardGrab import KeyboardGrab
from FileConvert import BinFileToJson


class BoshiCore:
    HOOK_LIBRARY_PATH = "BoshiKeyboard.dll" if os.name == "nt" else "keyboard.so"
    DEFAULT_MAPPING_FILE = "liu.bin"
    punctuationMapping = {
        "COMMA": ",",
        "DOT": ".",
        "LEFTBRACKET": "[",
        "RIGHTBRACKET": "]",
        "QUOTE": "'",
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
    alphaKeyMapping = {
        "KEYA": "a",
        "KEYB": "b",
        "KEYC": "c",
        "KEYD": "d",
        "KEYE": "e",
        "KEYF": "f",
        "KEYG": "g",
        "KEYH": "h",
        "KEYI": "i",
        "KEYJ": "j",
        "KEYK": "k",
        "KEYL": "l",
        "KEYM": "m",
        "KEYN": "n",
        "KEYO": "o",
        "KEYP": "p",
        "KEYQ": "q",
        "KEYR": "r",
        "KEYS": "s",
        "KEYT": "t",
        "KEYU": "u",
        "KEYV": "v",
        "KEYW": "w",
        "KEYX": "x",
        "KEYY": "y",
        "KEYZ": "z",
    }

    def __init__(self, callback):
        cur_path = os.path.abspath(os.path.curdir)

        dll_file = os.path.join(cur_path, self.HOOK_LIBRARY_PATH)
        KeyboardGrab.Hook(dll_file, self.handle_keyboard_event)

        bin_file = os.path.join(cur_path, self.DEFAULT_MAPPING_FILE)
        if os.path.exists(bin_file):
            self.wordMapping = BinFileToJson(bin_file)
        else:
            self.wordMapping = None
            logging.error(f"{bin_file} not found")

        self.inputBuffer = ""
        self.candidateList = []
        self.callback = callback

    def update_keyboard_grab(self):
        if not self.inputBuffer:
            KeyboardGrab.SetIntercept(2)
        else:
            KeyboardGrab.SetIntercept(1)

    def handle_ctrl_space(self):
        if KeyboardGrab.GetIntercept():
            KeyboardGrab.SetIntercept(0)
        else:
            KeyboardGrab.SetIntercept(2)
        self.inputBuffer = ""
        self.candidateList = []
        if self.callback:
            status = "1" if KeyboardGrab.GetIntercept() else "0"
            self.callback("SWITCH", [status])

    def handle_esc(self):
        self.inputBuffer = ""
        self.candidateList = []
        if self.callback:
            self.callback(self.inputBuffer, self.candidateList)
        self.update_keyboard_grab()

    def handle_selection(self, selection):
        assert self.inputBuffer != ""

        if self.candidateList and selection < len(self.candidateList):
            elect = self.candidateList[selection]
            KeyboardGrab.Output(elect)
        self.inputBuffer = ""
        self.candidateList = []
        if self.callback:
            self.callback(self.inputBuffer, self.candidateList)

    def handle_backspace(self):
        assert self.inputBuffer != ""

        self.inputBuffer = self.inputBuffer[:-1]
        self.candidateList = self.wordMapping.get(self.inputBuffer, [])
        if self.callback:
            self.callback(self.inputBuffer, self.candidateList)
        self.update_keyboard_grab()

    def handle_alpha(self, alpha):
        if alpha == "v" and self.candidateList:
            self.inputBuffer += alpha
            tempCandidateList = self.wordMapping.get(self.inputBuffer, [])
            if len(self.candidateList) < 2:
                self.candidateList = tempCandidateList
            else:
                self.candidateList = [self.candidateList[1]]
                if tempCandidateList:
                    self.candidateList.extend(tempCandidateList)
        else:
            self.inputBuffer += alpha
            self.candidateList = self.wordMapping.get(self.inputBuffer, [])
        if self.callback:
            self.callback(self.inputBuffer, self.candidateList)

    def handle_punctuation(self, punctuation):
        self.inputBuffer += punctuation
        self.candidateList = self.wordMapping.get(self.inputBuffer, [])
        if self.callback:
            self.callback(self.inputBuffer, self.candidateList)

    def handle_keyboard_event(self, msg_ptr):
        msg = msg_ptr.decode("utf-8")
        logging.debug(msg)

        if msg == "Ctrl+Space":
            self.handle_ctrl_space()

        if KeyboardGrab.GetIntercept() == 0:
            return

        if msg == "ESC":
            self.handle_esc()
        elif msg == "BACKSPACE":
            self.handle_backspace()
        elif msg == "SPACE":
            self.handle_selection(0)
        else:
            alpha = self.alphaKeyMapping.get(msg, None)
            digit = self.digitKeyMapping.get(msg, None)
            punctuation = self.punctuationMapping.get(msg, None)
            if alpha:
                self.handle_alpha(alpha)
            elif punctuation:
                self.handle_punctuation(punctuation)
            elif digit:
                self.handle_selection(int(digit))
        self.update_keyboard_grab()
        logging.debug(f"inputBuffer: {self.inputBuffer}")
        logging.debug(f"candidateList: {self.candidateList}")

    def SwitchLanguage(self):
        self.handle_ctrl_space()
