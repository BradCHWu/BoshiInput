import configparser
import os


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
            "Position": "100,100",
        }

    def SetPosition(self, pos: str):
        self._config.set("General", "Position", pos)

    def Position(self) -> str:
        return self._config.get("General", "Position")

    def Load(self) -> None:
        self._config.read(self._file_path, encoding="utf-8")

    def Save(self) -> None:
        with open(self._file_path, "w", encoding="utf-8") as ofile:
            self._config.write(ofile)
