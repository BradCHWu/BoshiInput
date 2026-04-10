import subprocess
import time


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

    import setting

    disp = [
        "uv",
        "run",
        "nuitka",
        "--standalone",
        "--onefile",
        "--enable-plugin=pyside6",
        "--windows-console-mode=disable",
        "--onefile-tempdir-spec={CACHE_DIR}\\" + setting.Name() + "_temp",
    ]
    if hasattr(setting, "Icon"):
        disp.append(f"--windows-icon-from-ico={setting.Icon()}")
    disp.append(f"--windows-company-name={setting.Author()}")
    disp.append("--include-windows-runtime-dlls=no")
    disp.append(f"--windows-product-name={setting.Name()}")
    ver = setting.Version().split(".")
    if len(ver) < 4:
        ver += ["0"] * (4 - len(ver))
    disp.append(f"--windows-file-version={'.'.join(ver)}")
    disp.append(f"--windows-product-version={'.'.join(ver)}")
    if hasattr(setting, "Description"):
        disp.append(f"--windows-file-description={setting.Description()}")
    disp.append(f"{setting.Name()}.py")
    p = subprocess.Popen(disp)
    while True:
        if p.poll() is None:
            time.sleep(0.1)
            continue
        break

    print(f"The execute file {setting.Name()} generated")
