import configparser
import os
import logging
from enum import Enum, auto
from tokenize import Name


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
            logging.info("Config instance created")
        return cls._instance

    def _load_config(self):
        cur_path = os.path.abspath(os.path.curdir)
        self._config_file = os.path.join(cur_path, self._file_name + ".ini")

        self._config = configparser.ConfigParser()
        self._config.optionxform = str

        self._language = LanguageSetting.CHINESE
        self._nextLanguage = {
            LanguageSetting.CHINESE: LanguageSetting.ENGLISH,
            LanguageSetting.ENGLISH: LanguageSetting.CHINESE,
        }
        if os.path.exists(self._config_file):
            self.Load()
        else:
            self._default_config()
            self.Save()

    def _initial_logging(self):
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
        logging_level = level
        logging_format = "[%(levelname)s] %(lineno)s %(message)s"
        if self._config.getboolean("General", "LoggingFile"):
            logging_file = f"{self._file_name}.log"
            logging.basicConfig(
                filename=logging_file,
                filemode="a",
                level=logging_level,
                format=logging_format,
            )
        else:
            logging.basicConfig(level=logging_level, format=logging_format)

    def _default_config(self):
        self._config["General"] = {
            "Logging": ["Debug", "Info", "Warning", "Error"],
            "LoggingLevel": "Debug",
            "LoggingFile": False,
            "Position": "100,100",
        }

    def SetPosition(self, pos: tuple):
        pos_str = f"{pos[0]},{pos[1]}"
        self._config.set("General", "Position", pos_str)

    def GetPosition(self) -> tuple:
        pos_str = self._config.get("General", "Position")
        pos = map(int, pos_str.split(","))
        return pos

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
        self._config.read(self._config_file, encoding="utf-8")

    def Save(self) -> None:
        with open(self._config_file, "w", encoding="utf-8") as ofile:
            self._config.write(ofile)


# 建立一個全域變數供其他模組匯入
config_manager = Config()
