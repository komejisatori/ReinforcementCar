import math
from typing import List

from car_game.src.core.geometry import Point, Line
import car_game.src.config.game as GAME_SETTING
from car_game.src.core.geometry import utils


class MovingBlock:
    start_pos: Point
    end_pos: Point
    size: int
    v: float
    period: float
    position: Point

    def __init__(self, start_pos: Point, end_pos: Point):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.size = GAME_SETTING.BLOCK_SIZE
        self.v = GAME_SETTING.BLOCK_V

        self.period = utils.distance_between_points(self.start_pos, self.end_pos) * 2 / self.v
        self.position = self.start_pos

    def update_position(self, game_lasting_time: float):
        half_period = self.period / 2.0
        t = math.fmod(game_lasting_time, self.period) / half_period

        if t <= 1:
            r = t
        else:
            r = 2 - t
        self.position = self.start_pos + (self.end_pos - self.start_pos).mul(r)


class EnvironmentMap:
    left_barrier_line: List[Point]
    right_barrier_line: List[Point]
    destination_line: Line
    block_list: List[MovingBlock]

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
        self.block_list = []

    def dist_to_destination(self, p: Point):
        index, offset = utils.get_closest_point(p, self.left_barrier_line)
        dist = offset + utils.calculate_length(self.left_barrier_line[index + 1:])
        return dist

    def create_moving_block(self, start_pos: Point, end_pos: Point):
        new_block = MovingBlock(start_pos, end_pos)
        self.block_list.append(new_block)

    def update_moving_block(self, game_lasting_time: float):
        for block in self.block_list:
            block.update_position(game_lasting_time)

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

