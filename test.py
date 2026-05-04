from OwlCore import OwlCore


def print_message(key, keyList):
    print(f"{key} --- {keyList}")


if __name__ == "__main__":
    boshiCore = OwlCore()
    boshiCore.HookKeybboard()
    boshiCore.InstallCallback(print_message)
    while True:
        pass
