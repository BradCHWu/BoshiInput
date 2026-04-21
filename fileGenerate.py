import subprocess
import os
import sys
import time
import setting

def fill_version(name, version) -> str:
    ver = version.split(".")
    if len(ver) < 4:
        ver += ["0"] * (4 - len(ver))

    author = setting.Author() if hasattr(setting, "Author") else "Brad Wu"
    if hasattr(setting, "Description"):
        description = setting.Description()
    else:
        name
    return f"""# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=({ver[0]}, {ver[1]}, {ver[2]}, {ver[3]}),
    prodvers=({ver[0]}, {ver[1]}, {ver[2]}, {ver[3]}),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x4,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
kids=[
    StringFileInfo(
    [
    StringTable(
        '040904e4',
        [StringStruct('Comments', ''),
        StringStruct('CompanyName', ''),
        StringStruct('FileDescription', f'{description}'),
        StringStruct('FileVersion', '1.0'),
        StringStruct('InternalName', f'{name}'),
        StringStruct('LegalCopyright', f'{author}'),
        StringStruct('OriginalFilename', f'{name}.exe'),
        StringStruct('ProductName', f'{name}'),
        StringStruct('ProductVersion', '{ver[0]}.{ver[1]}.{ver[2]}.{ver[3]}')])
    ]),
    VarFileInfo([VarStruct('Translation', [1033, 1252])])
]
)
"""


def update_setting():
    disp = [
        "uv",
        "run",
        "app_setting.py",
    ]
    p = subprocess.Popen(disp)
    while True:
        if p.poll() is None:
            time.sleep(0.1)
            continue
        break


if __name__ == "__main__":
    update_setting()

    results = fill_version(setting.Name(), setting.Version())
    info_file = "file_version_info.txt"
    with open(info_file, "w", encoding="utf-8") as ofile:
        ofile.write(results)

    disp = [
        "pyinstaller",
        "-w",
        "-F",
        setting.Name() + ".py",
        "-n",
        setting.Name()
    ]
    if hasattr(setting, "Icon"):
        disp.append("-i")
        disp.append(setting.Icon())
    disp.append("--paths=./")
    if sys.platform == "win32":
        disp.append(f"--version-file={info_file}")
    p = subprocess.Popen(disp)
    while True:
        if p.poll() is None:
            time.sleep(0.1)
            continue
        if os.path.exists(info_file):
            os.remove(info_file)
        break

    print(f"The execute file {setting.Name()} generated")
