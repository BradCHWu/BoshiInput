import sys

from QT.BoshiInputApp import BoshiInputApp


if __name__ == "__main__":
    app = BoshiInputApp(sys.argv)
    if app.status is None:
        sys.exit(app.exec())
    else:
        sys.exit(0)
