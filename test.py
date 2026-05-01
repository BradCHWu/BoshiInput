from BoshiCore import BoshiCore


def print_message(key, keyList):
    print(f"{key} --- {keyList}")


if __name__ == "__main__":
    boshiCore = BoshiCore()
    boshiCore.HookKeybboard()
    boshiCore.InstallCallback(print_message)
    while True:
        pass
