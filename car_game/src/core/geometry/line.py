from car_game.src.core.geometry import Point


class Line:
    """
    the line in the map
    """
    p1: Point
    p2: Point

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2