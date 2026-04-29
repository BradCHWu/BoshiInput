import wx


def toPoint(pos: str) -> wx.Point:
    p = [int(p) for p in pos.split(",")]
    return wx.Point(p[0], p[1])


def fromPoint(p: wx.Point) -> str:
    return f"{p.x},{p.y}"