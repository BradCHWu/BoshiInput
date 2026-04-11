import configparser
import os
import logging


class Config:
    _config = None
    _file_path = "BoshiInput.ini"

    def __init__(self):
        self._config = configparser.ConfigParser()
        self._config.optionxform = str

        if os.path.exists(self._file_path):
            self.Load()
        else:
            self._default_config()
            self.Save()

    def _default_config(self):
        self._config["General"] = {
            "Logging": ["Debug", "Info", "Warning", "Error"],
            "LoggingLevel": "Debug",
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

    def SetPosition(self, pos: str):
        self._config.set("General", "Position", pos)

    def Position(self) -> str:
        return self._config.get("General", "Position")

    def Load(self) -> None:
        self._config.read(self._file_path, encoding="utf-8")

    def Save(self) -> None:
        with open(self._file_path, "w", encoding="utf-8") as ofile:
            self._config.write(ofile)
