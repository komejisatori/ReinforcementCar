from typing import List

from core.geometry import Point
from core.car import Car
from core.observation import Observation, Reward


class EnvironmentMap:
    """
    the environment map info in the game
    """
    pass


class Barrier:
    x: int
    y: int
    width: int
    height: int

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Environment:
    """
    the environment information which contains barriers, destinations, etc
    """
    origin: Point
    destination: Point
    barrier_list: List[Barrier]

    def __init__(self, origin: Point, destination: Point, barrier_list: List[Barrier]):
        self.origin = origin
        self.destination = destination
        self.barrier_list = barrier_list

    @staticmethod
    def generate_default_barrier_list():
        pass

    def get_observation(self, player_car: Car):
        # TODO: fill with correct logic
        return Observation()

    def get_reward(self):
        # TODO: fill with correct logic
        return Reward()

    def get_terminal(self):
        # TODO: fill with correct logic
        return 0
