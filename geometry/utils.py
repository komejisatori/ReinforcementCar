import math

from geometry.point import Point


def rotate(p, a):
    return Point(
        p.x * math.cos(a) - p.y * math.sin(a),
        p.x * math.sin(a) + p.y * math.cos(a),
    )
