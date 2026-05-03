import configparser
import os
import logging
import datetime
from enum import Enum, auto

from BoshiCore import BoshiCore


class LanguageSetting(Enum):
    CHINESE = auto()
    ENGLISH = auto()


class Config:
    _instance = None
    _config = None
    _file_name = "BoshiInput"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
            cls._instance._initial_logging()
            cls._boshiCore = None
            logging.info("Config instance created")
        return cls._instance

    def _load_config(self):
        cur_path = os.path.abspath(os.path.curdir)
        self._config_file = os.path.join(cur_path, self._file_name + ".ini")

        self._config = configparser.ConfigParser()
        self._config.optionxform = str
        if os.path.exists(self._config_file):
            self.Load()
        else:
            self._default_config()
            self.Save()

    def _initial_logging(self):
        _logging = self._config["Logging"]
        if _logging["Level"] not in _logging["Lists"]:
            _logging["Level"] = "Info"
            self.Save()

        level = logging.INFO
        match _logging["Level"]:
            case "Debug":
                level = logging.DEBUG
            case "Info":
                level = logging.INFO
            case "Warning":
                level = logging.WARNING
            case "Error":
                level = logging.ERROR
        logging_level = level
        logging_format = (
            "[%(levelname)s] %(filename)s %(funcName)s %(lineno)s %(message)s"
        )
        if self._config.getboolean("Logging", "File"):
            now = datetime.datetime.now().strftime("%Y-%m-%d-%H%M-%S")
            logging_file = f"{self._file_name}_{now}.log"
            logging.basicConfig(
                filename=logging_file,
                filemode="w",
                level=logging_level,
                format=logging_format,
            )
        else:
            logging.basicConfig(level=logging_level, format=logging_format)

    def _default_config(self):
        self._config["Logging"] = {
            "Lists": ["Debug", "Info", "Warning", "Error"],
            "Level": "Info",
            "File": True,
        }
        self._config["General"] = {
            "Position": "100,100",
            "Cadidate": 4,
        }

    def SetPosition(self, pos: tuple):
        pos_str = f"{pos[0]},{pos[1]}"
        self._config.set("General", "Position", pos_str)

    def GetPosition(self) -> tuple:
        pos_str = self._config.get("General", "Position")
        pos = map(int, pos_str.split(","))
        return pos

    def SetCadidateNumber(self, num) -> None:
        self._config.set("General", "Cadidate", f"{num}")
        if self._boshiCore:
            self._boshiCore.SetCandidateNumber(num)

    def GetCadidateNumber(self) -> int:
        return self._config.getint("General", "Cadidate")

    def Load(self) -> None:
        self._config.read(self._config_file, encoding="utf-8")

    def Save(self) -> None:
        with open(self._config_file, "w", encoding="utf-8") as ofile:
            self._config.write(ofile)

    def InstallCallback(self, callback):
        self._boshiCore = BoshiCore()
        self._boshiCore.HookKeybboard()
        self._boshiCore.InstallCallback(callback)

        num = self.GetCadidateNumber()
        self._boshiCore.SetCandidateNumber(num)

    def UninstallCallback(self):
        self._boshiCore.UnhookKeyboard()
        self._boshiCore = None

    def SwitchLanguage(self):
        if self._boshiCore:
            self._boshiCore.SwitchLanguage()


# 建立一個全域變數供其他模組匯入
config_manager = Config()
