from enum import Enum

from geometry.point import Point


class Car:
    def __init__(self):
        self.reset()

    def reset(self):
        self.pos = Point(0.0, 0.0)
        self.velocity = 0.0


class Action(Enum):
    Idle = 0
    Left = 1
    Right = 2


class Status(Enum):
    NotStarted = 0
    Running = 1
    Failed = 2
    Success = 3
    Destroyed = 4


class Game:
    def __init__(self):
        self.status = Status.NotStarted
        self.car = STANDARD_CAR

    def step(self, action):
        assert self.status == Status.Running

    def reset(self):
        self.status = Status.Running
        self.car = STANDARD_CAR

    def destroy(self):
        self.status = Status.Destroyed
