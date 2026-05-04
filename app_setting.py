import base64
import os
import sys
import tomllib


def Header() -> str:
    return "import base64"


def Name(name) -> str:
    return f'def Name() -> str:\n    return "{name}"'


def Version(version) -> str:
    return f'def Version() -> str:\n    return "{version}"'


def Icon(icon) -> str:
    return f'def Icon() -> str:\n    return r"{icon}"'


def Author(author) -> str:
    return f'def Author() -> str:\n    return "{author}"'


def Description(description) -> str:
    return f'def Description() -> str:\n    return "{description}"'


def Code(module) -> str:
    codeList = []
    if module == "W":
        codeList.append("import io")
        codeList.append("import wx")
        codeList.append("")
        codeList.append("")
        codeList.append("def LoadPNG(png) -> wx.Icon:")
        codeList.append("    image_data = base64.b64decode(png)")
        codeList.append("    stream = io.BytesIO(image_data)")
        codeList.append("    image = wx.Image(stream, wx.BITMAP_TYPE_PNG)")
        codeList.append("    icon = wx.Icon(wx.Bitmap(image))")
        codeList.append("    return icon")
    elif module == "Q":
        codeList.append("from PySide6.QtGui import QPixmap")
        codeList.append("")
        codeList.append("")
        codeList.append("def LoadPNG(png) -> QPixmap:")
        codeList.append("    pixmap = QPixmap()")
        codeList.append("    pixmap.loadFromData(base64.b64decode(png))")
        codeList.append("    return pixmap")
    return "\n".join(codeList)


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

        app = wx.App()
        if app.IsActive():
            print("wx.App created for icon conversion")

        image = wx.Image(png_path)
        if not image.IsOk():
            print(f"錯誤：無法載入圖片 '{png_path}'。")
            return False
        max_scale = max(size[0] for size in sizes)
        scaled_image = image.Scale(max_scale, max_scale)
        return scaled_image.SaveFile(icon_path, wx.BITMAP_TYPE_ICO)
    except ImportError:
        return False


def __icon_from_pyside6(png_path, icon_path, sizes):
    try:
        import sys
        from PySide6.QtGui import QImage, QPixmap
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt

        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)

        image = QImage(png_path)
        if image.isNull():
            print(f"錯誤：無法載入圖片 '{png_path}'。")
            return False
        max_scale = max(size[0] for size in sizes)
        scaled_pixmap = QPixmap.fromImage(image).scaled(
            max_scale,
            max_scale,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        return scaled_pixmap.save(icon_path, "ICO")
    except ImportError:
        return False


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


def get_image_list(toml, tool, name):
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


def convert_icon(toml, tool, name, imageList, module):
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
        png = image
        ico = icon_name + ".ico"
        sizes = ((32, 32), (64, 64))
        if module == "W" and __icon_from_wx(png, ico, sizes):
            print(f"成功使用 wxPython 將 '{png}' 轉換成 '{ico}'")
        elif module == "Q" and __icon_from_pyside6(png, ico, sizes):
            print(f"成功使用 PySide6 將 '{png}' 轉換成 '{ico}'")
        elif __icon_from_pil(png, ico, sizes):
            print(f"成功使用 PIL 將 '{png}' 轉換成 '{ico}'")
        else:
            print(f"錯誤：無法將 '{png}' 轉換為 '{ico}'")
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
SETTING = "setting.py"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Use 'app_setting W' or 'app_setting Q' to generate setting")
        sys.exit()

    MODULE = sys.argv[1]
    name, version = __extract_toml(TOML)
    if name and version:
        imageList = get_image_list(TOML, TOOL, name)
        if imageList:
            icon = convert_icon(TOML, TOOL, name, imageList, MODULE)
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
            codeList.append(Code(MODULE))
            for image in imageList:
                filename = os.path.split(image)[-1]
                name = os.path.splitext(filename)[0]
                for ch in ("-", " "):
                    if ch in name:
                        name = name.replace(ch, "_")
                codeList.append(f"png_{name} = {__png_to_base64(image)}")

        cur = os.path.join(os.path.curdir, MODULE)
        if not os.path.exists(cur):
            os.makedirs(cur)
        setting_file = os.path.join(MODULE, SETTING)
        with open(setting_file, "w", newline="", encoding="utf-8") as ofile:
            ofile.write("\n\n\n".join(codeList))
