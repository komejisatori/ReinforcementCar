from enum import Enum
import time

import config.resource as RESOURCE
import config.game as GAME_SETTING

from core.car import Car, CarControlAction, CarTerminal
from core.enviroment import EnvironmentMap
from core.geometry import Point


class GameStatus(Enum):
    NotStarted = 0
    Running = 1
    Failed = 2
    Success = 3
    Destroyed = 4


class CarGame:
    # game_engine: CarGameEngine
    player_car: Car
    environment_map: EnvironmentMap
    game_status: GameStatus

    def __init__(self):
        self.game_status = GameStatus.Running
        self._init_player_car()
        self._init_environment_map()

    def _init_player_car(self):
        self.player_car = Car()

    def _init_environment_map(self):
        self.environment_map = EnvironmentMap()

    def run(self):
        # Main Loop
        i = 0
        while True:
            if GAME_SETTING.List[i] == 0:
                self.step(action=CarControlAction.ACTION_IDLE, training=True)
                # print("idle")
            elif GAME_SETTING.List[i] == 1:
                self.step(action=CarControlAction.ACTION_TURN_LEFT, training=True)
                # print("left")
            elif GAME_SETTING.List[i] == 2:
                self.step(action=CarControlAction.ACTION_TURN_RIGHT, training=True)
                # print("right")

            # self.player_car.output_car_info()
            time.sleep(1.0 / GAME_SETTING.GAME_STEP_INTERVAL)
            i = (i + 1) % len(GAME_SETTING.List)

    def step(self, action: CarControlAction, training=True):
        """
        one step
        :param action:
        :param training:
        :return:
        """
        assert self.game_status == GameStatus.Running
        if not training:
            pass
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         exit()
            #     if event.type == KEYDOWN:
            #         self._deal_with_key_down(event)
        else:
            self.player_car.receive_control(action)
            observation, reward, terminal = self.player_car.calculate_observation_reward_terminal(self.environment_map)
            if terminal == CarTerminal.Failed:
                self.game_status = GameStatus.Failed
            elif terminal == CarTerminal.Success:
                self.game_status = GameStatus.Success

            return observation, reward, terminal



    def reset(self):
        self.player_car.reset_car()
        self.game_status = GameStatus.Running

    def destroy(self):
        self.game_status = GameStatus.Destroyed


def start_game():
    car_game_instance = CarGame()
    car_game_instance.run()
