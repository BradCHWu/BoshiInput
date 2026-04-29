import sys

from QT.BoshiInputApp import BoshiInputApp


if __name__ == "__main__":
    app = BoshiInputApp(sys.argv)
    if not app.status:
        sys.exit(0)
    sys.exit(app.exec())
