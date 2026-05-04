import os
import logging
from enum import Enum

from KeyboardGrab import KeyboardGrab
from FileConvert import BoiFileToJson


class LanguageSetting(Enum):
    ENGLISH = "0"
    TRADITIONAL = "1"
    SIMPLIFIED = "2"
    TAIWANESE = "3"
    JAPANESE = "4"


class OwlCore:
    HOOK_LIBRARY_PATH = "owl_keyboard.dll" if os.name == "nt" else "owl_keyboard.so"
    DEFAULT_MAPPING_FILE = "liu.boi"
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

    def __init__(self):
        self.isHook = False

        cur_path = os.path.abspath(os.path.curdir)
        boi_file = os.path.join(cur_path, self.DEFAULT_MAPPING_FILE)
        if os.path.exists(boi_file):
            self.wordMapping = BoiFileToJson(boi_file)
        else:
            self.wordMapping = None
            logging.error(f"{boi_file} not found")

        self.inputBuffer = ""
        self.candidateList = []
        self.candidateNumber = 4
        self.callback = None
        self.pageIndex = 1
        self.languageSetting = LanguageSetting.TRADITIONAL

    def send_callback(self):
        total = len(self.candidateList)
        if total <= self.candidateNumber:
            key = self.inputBuffer
            keyList = self.candidateList
        else:
            pageCount = (total - 1) // self.candidateNumber + 1
            if self.pageIndex <= 0:
                self.pageIndex += pageCount
            elif self.pageIndex > pageCount:
                self.pageIndex -= pageCount
            temp = [self.inputBuffer]
            temp.append(f"{self.pageIndex}/{pageCount}")
            key = "|".join(temp)
            s = self.candidateNumber * (self.pageIndex - 1)
            e = s + self.candidateNumber
            keyList = self.candidateList[s:e]

        if self.callback:
            self.callback(key, keyList)
        msg = 1 if self.inputBuffer else 2
        KeyboardGrab.SetIntercept(msg)

    def send_switch(self):
        self.inputBuffer = ""
        self.candidateList = []
        self.pageIndex = 1
        if self.callback:
            if KeyboardGrab.GetIntercept() == 0:
                status = LanguageSetting.ENGLISH.value
            else:
                status = self.languageSetting.value
            self.callback("SWITCH", [status])

    def handle_ctrl_space(self):
        if KeyboardGrab.GetIntercept():
            KeyboardGrab.SetIntercept(0)
        else:
            KeyboardGrab.SetIntercept(2)

        self.send_switch()

    def handle_esc(self):
        self.inputBuffer = ""
        self.candidateList = []
        self.pageIndex = 1
        self.send_callback()

    def handle_backspace(self):
        mapping = self.wordMapping[self.languageSetting.value]

        self.inputBuffer = self.inputBuffer[:-1]
        self.candidateList = mapping.get(self.inputBuffer, [])
        self.pageIndex = 1
        self.send_callback()

    def handle_selection(self, selection):
        langMapping = {
            ",,t": LanguageSetting.TRADITIONAL,
            ",,c": LanguageSetting.SIMPLIFIED,
            ",,ct": LanguageSetting.TAIWANESE,
            ",,j": LanguageSetting.JAPANESE,
        }
        lang = langMapping.get(self.inputBuffer, None)
        if lang is None:
            s = self.candidateNumber * (self.pageIndex - 1)
            e = s + self.candidateNumber
            keyList = self.candidateList[s:e]
            if self.candidateList and selection < len(keyList):
                elect = keyList[selection]
                KeyboardGrab.Output(elect)
            self.inputBuffer = ""
            self.candidateList = []
            self.send_callback()
        else:
            self.languageSetting = lang
            self.send_switch()

    def handle_left(self):
        self.pageIndex -= 1
        self.send_callback()

    def handle_right(self):
        self.pageIndex += 1
        self.send_callback()

    def handle_alpha(self, alpha):
        mapping = self.wordMapping[self.languageSetting.value]

        if alpha == "v" and self.candidateList:
            self.inputBuffer += alpha
            tempCandidateList = mapping.get(self.inputBuffer, [])
            if len(tempCandidateList) > 0:
                self.candidateList = tempCandidateList
            elif len(self.candidateList) > 1:
                self.candidateList = [self.candidateList[1]]
            else:
                logging.warning(f"No candidate for {self.inputBuffer}")
                self.inputBuffer = ""
                self.candidateList = []
        else:
            self.inputBuffer += alpha
            self.candidateList = mapping.get(self.inputBuffer, [])
        self.pageIndex = 1
        self.send_callback()

    def handle_punctuation(self, punctuation):
        mapping = self.wordMapping[self.languageSetting.value]

        self.inputBuffer += punctuation
        self.candidateList = mapping.get(self.inputBuffer, [])
        self.pageIndex = 1
        self.send_callback()

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
        elif msg == "LEFT":
            self.handle_left()
        elif msg == "RIGHT":
            self.handle_right()
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
        self.send_callback()
        logging.debug(f"inputBuffer: {self.inputBuffer}")
        logging.debug(f"candidateList: {self.candidateList}")

    def HookKeybboard(self):
        if self.isHook:
            logging.error("Has hooked")
            return

        cur_path = os.path.abspath(os.path.curdir)
        dll_file = os.path.join(cur_path, self.HOOK_LIBRARY_PATH)
        KeyboardGrab.Hook(dll_file, self.handle_keyboard_event)
        logging.info(f"Hook to {dll_file}")
        self.isHook = True

    def UnhookKeyboard(self):
        if not self.isHook:
            logging.error("No hook")
            return

        KeyboardGrab.Unhook()
        logging.info("Unhook")
        self.isHook = False

    def SetCandidateNumber(self, num):
        self.candidateNumber = num

    def GetCandidateNumber(self):
        return self.candidateNumber

    def InstallCallback(self, callback):
        self.callback = callback

    def SwitchLanguage(self):
        self.handle_ctrl_space()
