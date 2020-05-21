from enum import Enum
import time

import config.resource as RESOURCE
import config.game as GAME_SETTING

from core.car import Car, CarControlAction, CarTerminal
from core.enviroment import EnvironmentMap
from core.geometry import Point
import pygame
from pygame.locals import *

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
        self._init_game()
        self._init_player_car()
        self._init_environment_map()
        self._init_render()

    def _init_player_car(self):
        self.player_car = Car()

    def _init_environment_map(self):
        self.environment_map = EnvironmentMap()

    def _init_game(self):
        pygame.init()
        img_icon = pygame.image.load(RESOURCE.IMAGE_ICON_FILE_PATH)
        pygame.display.set_icon(img_icon)
        pygame.display.set_caption(GAME_SETTING.GAME_TITLE)

    def _init_render(self):
        self.map_width, self.map_height = GAME_SETTING.GAME_SCREEN_WIDTH, GAME_SETTING.GAME_SCREEN_HEIGHT
        self.map_size = self.map_width, self.map_height
        self.screen = pygame.display.set_mode(self.map_size)
        self.color_bg = (255, 255, 255)
        # self.img_car = pygame.image.load(RESOURCE.IMAGE_CAR_FILE_PATH)
        # self.img_car = pygame.transform.scale(self.img_car, (GAME_SETTING.GAME_CAR_WIDTH, GAME_SETTING.GAME_CAR_HEIGHT))
        # self.player_car_position = self.img_car.get_rect()
        # self.player_car_start_point = Point(20, 20)

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
                print("right")

            self.player_car.output_car_info()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == KEYDOWN:
                    pass
            self.render()
            # time.sleep(1.0 / GAME_SETTING.GAME_STEP_INTERVAL)
            pygame.time.delay(GAME_SETTING.GAME_STEP_INTERVAL)
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

    def render(self):
        self._render_background()
        self._render_environment(self.environment_map)
        self._render_cars(self.player_car)
        #self._render_player_car(self.player_car)
        pygame.display.flip()

    def _render_background(self):
        self.screen.fill(self.color_bg)

    def _render_environment(self, environment:EnvironmentMap, color=(0,0,0)):
        left_lines = [p.to_pair() for p in environment.left_barrier_line]
        right_lines = [p.to_pair() for p in environment.right_barrier_line]
        pygame.draw.lines(self.screen, color, False, left_lines)
        pygame.draw.lines(self.screen, color, False, right_lines)
        des_line = environment.destinationLine
        color_des = (255, 210, 0)
        pygame.draw.line(self.screen, color_des, des_line.p1.to_pair(), des_line.p2.to_pair())

    def _render_cars(self, car:Car, color=(0,0,0)):
        car_position = (car.position.x, car.position.y)
        car_size = (car.width, car.height)
        car_rect = pygame.Rect(car_position, car_size)
        pygame.draw.rect(self.screen, color, car_rect, 1)

    # def _render_player_car(self, player_car):
    #     position_delta = [
    #         player_car.position.x - self.player_car_position.left,
    #         player_car.position.y - self.player_car_position.top
    #     ]
    #     self.player_car_position = self.player_car_position.move(position_delta)
    #     self.screen.blit(self.img_car, self.player_car_position)


def start_game():
    car_game_instance = CarGame()
    car_game_instance.run()
