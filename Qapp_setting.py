import base64
import os
import tomllib


def Header() -> str:
    return "import base64\n\nfrom PySide6.QtGui import QPixmap"


def Name(name) -> str:
    return f'def Name() -> str:\n    return "{name}"'


def Version(version) -> str:
    return f'def Version() -> str:\n    return "{version}"'


def Icon(icon) -> str:
    return f'def Icon() -> str:\n    return r"{icon}"'


def Code() -> str:
    return """def LoadPNG(png) -> QPixmap:
    pixmap = QPixmap()
    pixmap.loadFromData(base64.b64decode(png))
    return pixmap
"""


def Author(author) -> str:
    return f'def Author() -> str:\n    return "{author}"'


def Description(description) -> str:
    return f'def Description() -> str:\n    return "{description}"'


def __valid_png(folder):
    if not os.path.exists(folder):
        print(f"The folder {folder} does not exist")
        return
    pngList = list()
    for png in os.listdir(folder):
        _, ext = os.path.splitext(png)
        if ext.lower() != ".png":
            continue
        pngList.append(os.path.join(folder, png))
    return pngList


def __png_to_base64(png):
    return base64.b64encode(open(png, "rb").read())


def __icon_from_pil(png_path, icon_path, sizes):
    try:
        from PIL import Image

        img = Image.open(png_path)
        img.save(icon_path, format="ICO", sizes=sizes)
    except ImportError:
        return False
    return True


def __icon_from_wx(png_path, icon_path, sizes):
    try:
        import wx

        image = wx.Image(png_path, wx.BITMAP_TYPE_PNG)
        if not image.IsOk():
            print(f"錯誤：無法載入圖片 '{png_path}'。")
            return False
        
        # wxPython doesn't directly support ICO saving, but we can use PIL as primary
        # For now, return False to fall back to other methods
        return False
    except ImportError:
        return False


def PngToIco(png_path, ico_path, sizes=((16, 16), (32, 32), (48, 48))):
    """
    將 PNG 檔案轉換為 ICO 檔案。

    Args:
        png_path (str): 輸入的 PNG 檔案路徑。
        ico_path (str): 輸出的 ICO 檔案路徑。
        sizes (tuple): 包含要用於 ICO 檔案的尺寸元組，例如 ((16, 16), (32, 32))。
    """
    if not os.path.exists(png_path):
        print(f"錯誤：找不到檔案 '{png_path}'。")
        return

    if __icon_from_pil(png_path, ico_path, sizes):
        print(f"成功將 '{png_path}' 轉換為 '{ico_path}' by PIL")
    elif __icon_from_wx(png_path, ico_path, sizes):
        print(f"成功將 '{png_path}' 轉換為 '{ico_path}' by wxPython")
    else:
        print(f"錯誤：無法將 '{png_path}' 轉換為 '{ico_path}'")


def __toml_config(toml):
    if not os.path.exists(toml):
        print(f"The toml file {toml} does not exist")
        return None

    with open(toml, "rb") as ifile:
        config = tomllib.load(ifile)

    return config


def __extract_toml(toml):
    config = __toml_config(toml)
    if config is None:
        return None, None

    if "project" not in config:
        print(f"{'project'} does not exist in {toml}")
        return None, None

    if "name" not in config["project"]:
        print(f"{'name'} does not exist in {toml} under {'project'}")
        return None, None

    if "version" not in config["project"]:
        print(f"{'version'} does not exist in {toml} under {'project'}")
        return None, None

    return config["project"]["name"], config["project"]["version"]


def convert_image(toml, tool, name):
    config = __toml_config(toml)
    if tool not in config:
        print(f"{tool} does not exist in {toml}")
        return None

    if name not in config[tool]:
        print(f"{name} does not exist in {toml} under {tool}")
        return None

    if "images" not in config[tool][name]:
        print(f"{'images'} does not exist in {toml} under {tool}.{name}")
        return None

    images = config[tool][name]["images"]
    imageList = __valid_png(images)
    if not imageList:
        print("No any images exist. Please add png files")
        return None

    return imageList


def convert_icon(toml, tool, name, imageList):
    config = __toml_config(toml)
    if tool not in config:
        print(f"{tool} does not exist in {toml}")
        return None

    if name not in config[tool]:
        print(f"{name} does not exist in {toml} under {tool}")
        return None

    icon = config[tool][name]["icon"]
    if not icon:
        print("No icon setting, skip it...")
        return None

    icon_name = os.path.splitext(icon)[0]
    for image in imageList:
        if icon_name not in os.path.splitext(image)[0]:
            continue
        PngToIco(image, icon_name + ".ico")
        break

    return icon


def convert_author(toml, tool, name):
    config = __toml_config(toml)
    if tool not in config:
        print(f"{tool} does not exist in {toml}")
        return None

    if name not in config[tool]:
        print(f"{name} does not exist in {toml} under {tool}")
        return None

    if "author" not in config[tool][name]:
        print(f"{'author'} does not exist in {toml} under {tool}.{name}")
        return None

    return config[tool][name]["author"]


def convert_description(toml, tool, name):
    config = __toml_config(toml)
    if tool not in config:
        print(f"{tool} does not exist in {toml}")
        return None

    if name not in config[tool]:
        print(f"{name} does not exist in {toml} under {tool}")
        return None

    if "description" not in config[tool][name]:
        print(f"{'description'} does not exist in {toml} under {tool}.{name}")
        return None

    return config[tool][name]["description"]


TOML = "pyproject.toml"
TOOL = "tool"
MODULE = "QT"
SETTING = "setting.py"

if __name__ == "__main__":
    name, version = __extract_toml(TOML)
    if name and version:
        imageList = convert_image(TOML, TOOL, name)
        if imageList:
            icon = convert_icon(TOML, TOOL, name, imageList)
        author = convert_author(TOML, TOOL, name)
        description = convert_description(TOML, TOOL, name)

        codeList = list()
        if imageList:
            codeList.append(Header())
        codeList.append(Name(name))
        codeList.append(Version(version))
        if author:
            codeList.append(Author(author))
        if description:
            codeList.append(Description(description))

        if icon:
            codeList.append(Icon(icon))
        if imageList:
            codeList.append(Code())
            for image in imageList:
                filename = os.path.split(image)[-1]
                name = os.path.splitext(filename)[0]
                for ch in ("-", " "):
                    if ch in name:
                        name = name.replace(ch, "_")
                codeList.append(f"png_{name} = {__png_to_base64(image)}")

        setting_file = os.path.join(MODULE, SETTING)
        with open(setting_file, "w", newline="", encoding="utf-8") as ofile:
            ofile.write("\n\n\n".join(codeList))
