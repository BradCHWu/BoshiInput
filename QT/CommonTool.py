from PySide6.QtCore import QPoint


def toQPoint(pos: str) -> QPoint:
    p = [int(p) for p in pos.split(",")]
    return QPoint(p[0], p[1])


def fromQPoint(p: QPoint) -> str:
    return f"{p.x()},{p.y()}"
