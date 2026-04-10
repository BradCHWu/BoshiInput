from PySide6.QtWidgets import QMainWindow
from setting import LoadPNG, png_Boshi

class MainFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(LoadPNG(png_Boshi))