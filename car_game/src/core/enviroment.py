from typing import List

from core.geometry import Point, Line
import config.game as GAME_SETTING
from core.geometry import utils

class EnvironmentMap:
    left_barrier_line: List[Point]
    right_barrier_line: List[Point]
    destination_line: Line

    total_length: float

    def __init__(self):
        self.left_barrier_line = []
        self.right_barrier_line = []

        for (x, y) in GAME_SETTING.BARRIER_LEFT_LINE:
            self.left_barrier_line.append(Point(x, y))
        for (x, y) in GAME_SETTING.BARRIER_RIGHT_LINE:
            self.right_barrier_line.append(Point(x, y))

        self.destinationLine = Line(self.left_barrier_line[-1], self.right_barrier_line[-1])
        self.total_length = utils.calculate_length(self.left_barrier_line)

    def dist_to_destination(self, p: Point):
        index, offset = utils.get_closest_point(p, self.left_barrier_line)
        dist = offset + utils.calculate_length(self.left_barrier_line[index + 1:])
        return dist
