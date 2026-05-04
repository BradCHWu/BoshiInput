import sys

from Q.OwlInputApp import OwlInputApp


if __name__ == "__main__":
    app = OwlInputApp(sys.argv)
    if not app.status:
        sys.exit(0)
    sys.exit(app.exec())
