from typing import List

from car_game.src.core.geometry import Point, Line
import car_game.src.config.game as GAME_SETTING
from car_game.src.core.geometry import utils

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

        self.build_destination_line()
        self.total_length = utils.calculate_length(self.left_barrier_line)

    def dist_to_destination(self, p: Point):
        index, offset = utils.get_closest_point(p, self.left_barrier_line)
        dist = offset + utils.calculate_length(self.left_barrier_line[index + 1:])
        return dist

    def build_destination_line(self):
        self.destinationLine = Line(self.left_barrier_line[-1], self.right_barrier_line[-1])

    def extend_left_barrier_line(self, point: Point):
        self.left_barrier_line.append(point)

    def extend_right_barrier_line(self, point: Point):
        self.right_barrier_line.append(point)

    def cut_left_barrier_line(self):
        if len(self.left_barrier_line) > 0:
            self.left_barrier_line.pop()

    def cut_right_barrier_line(self):
        if len(self.right_barrier_line) > 0:
            self.right_barrier_line.pop()