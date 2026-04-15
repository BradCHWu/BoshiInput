import configparser
import os
import logging
from enum import Enum, auto


class LanguageSetting(Enum):
    CHINESE = auto()
    ENGLISH = auto()


class Config:
    _instance = None
    _config = None
    _file_path = "BoshiInput.ini"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        self._config = configparser.ConfigParser()
        self._config.optionxform = str
        self._language = LanguageSetting.CHINESE
        self._nextLanguage = {
            LanguageSetting.CHINESE: LanguageSetting.ENGLISH,
            LanguageSetting.ENGLISH: LanguageSetting.CHINESE,
        }

        if os.path.exists(self._file_path):
            self.Load()
        else:
            self._default_config()
            self.Save()

    def _default_config(self):
        self._config["General"] = {
            "Logging": ["Debug", "Info", "Warning", "Error"],
            "LoggingLevel": "Debug",
            "LoggingFile": False,
            "Position": "100,100",
        }

    def LoggingLevel(self):
        general = self._config["General"]
        if general["LoggingLevel"] not in general["Logging"]:
            general["LoggingLevel"] = "Info"
            self.Save()

        level = logging.INFO
        match general["LoggingLevel"]:
            case "Debug":
                level = logging.DEBUG
            case "Info":
                level = logging.INFO
            case "Warning":
                level = logging.WARNING
            case "Error":
                level = logging.ERROR
        return level

    def LoggingFile(self):
        return self._config.getboolean("General", "LoggingFile")

    def SetPosition(self, pos: str):
        self._config.set("General", "Position", pos)

    def Position(self) -> str:
        return self._config.get("General", "Position")

    def IsEnglish(self) -> bool:
        return self._language == LanguageSetting.ENGLISH

    def NextLanguage(self) -> LanguageSetting:
        self._language = self._nextLanguage[self._language]
        return self.Language()

    def Language(self) -> LanguageSetting:
        return self._language

    def ShowLanguage(self) -> str:
        mapping = {LanguageSetting.CHINESE: "中", LanguageSetting.ENGLISH: "英"}
        return mapping.get(self._language, "英")

    def Load(self) -> None:
        self._config.read(self._file_path, encoding="utf-8")

    def Save(self) -> None:
        with open(self._file_path, "w", encoding="utf-8") as ofile:
            self._config.write(ofile)


# 建立一個全域變數供其他模組匯入
config_manager = Config()
