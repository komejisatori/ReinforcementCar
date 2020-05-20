from enum import Enum

import pygame
import sys
from pygame.locals import *

import config.resource as RESOURCE
import config.game as GAME_SETTING

from core.car import Car, CarControlAction
from core.enviroment import Environment
from core.base import Position

from core.observation import Observation, Reward


class CarGameEngine:
    def __init__(self):
        self._init_setting()

    def _init_setting(self):
        pygame.init()
        pygame.display.set_caption(GAME_SETTING.GAME_TITLE)
        img_icon = pygame.image.load(RESOURCE.IMAGE_ICON_FILE_PATH)
        pygame.display.set_icon(img_icon)

        # screen
        self.map_width, self.map_height = GAME_SETTING.GAME_SCREEN_WIDTH, GAME_SETTING.GAME_SCREEN_HEIGHT
        self.map_size = self.map_width, self.map_height
        self.screen = pygame.display.set_mode(self.map_size)

        # background
        self.color_bg = (199, 237, 204)

        # player car
        self.img_car = pygame.image.load(RESOURCE.IMAGE_CAR_FILE_PATH)
        self.img_car = pygame.transform.scale(self.img_car, (GAME_SETTING.GAME_CAR_WIDTH, GAME_SETTING.GAME_CAR_HEIGHT))
        self.player_car_position = self.img_car.get_rect()
        # TODO: fill logic of start point
        self.player_car_start_point = Position(20, 20)

    def _render_cover(self):
        """
        not used for now
        :return:
        """
        self.img_cover = pygame.image.load(RESOURCE.IMAGE_COVER_FILE_PATH)
        self.img_cover = pygame.transform.scale(self.img_cover, (GAME_SETTING.GAME_SCREEN_WIDTH, GAME_SETTING.GAME_SCREEN_HEIGHT))
        self.screen.blit(self.img_cover, self.img_cover.get_rect())
        pygame.display.flip()
        pygame.time.delay(GAME_SETTING.GAME_STEP_INTERVAL)


    def render(self, player_car: Car, environment: Environment):
        # fill bg
        self._render_background()
        # fill environment
        self._render_environment(environment)
        # update player car
        self._render_player_car(player_car)

        pygame.display.flip()
        pygame.time.delay(GAME_SETTING.GAME_STEP_INTERVAL)

    def _render_background(self):
        self.screen.fill(self.color_bg)

    def _render_environment(self, environment: Environment):
        # TODO: fill with logic
        pass

    def _render_player_car(self, player_car):
        position_delta = [
            player_car.position.x - self.player_car_position.left,
            player_car.position.y - self.player_car_position.top
        ]
        self.player_car_position = self.player_car_position.move(position_delta)
        self.screen.blit(self.img_car, self.player_car_position)


class GameStatus(Enum):
    NotStarted = 0
    Running = 1
    Failed = 2
    Success = 3
    Destroyed = 4


class CarGame:
    game_engine: CarGameEngine
    player_car: Car
    environment: Environment
    game_status: GameStatus

    def __init__(self):
        self.game_status = GameStatus.NotStarted
        self.reset()

    def _init_game_engine(self):
        self.game_engine = CarGameEngine()

    def _init_player_car(self):
        self.player_car = Car(self.game_engine.player_car_start_point, GAME_SETTING.GAME_CAR_WIDTH,
                              GAME_SETTING.GAME_CAR_HEIGHT)

    def _init_environment(self):
        self.environment = Environment(None, None, None)

    def run(self):
        # Main Loop
        while True:
            self.step(action=CarControlAction.ACTION_IDLE, training=False)

    def step(self, action: CarControlAction, training=True):
        """
        one step
        :param action:
        :param training:
        :return:
        """
        assert self.game_status == GameStatus.Running
        if not training:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == KEYDOWN:
                    self._deal_with_key_down(event)
        else:
            self._deal_with_action(action)

        self._move_player_car()
        self.game_engine.render(self.player_car, self.environment)
        return self.environment.get_observation(
            self.player_car), self.environment.get_reward(), self.environment.get_terminal()

    def _deal_with_key_down(self, event):
        """
        deal with the key down event
        :param event:
        :return:
        """
        if event.key == K_LEFT:
            print(f'[event] left key pushed.')
            self.player_car.turn_left()

        if event.key == K_RIGHT:
            print(f'[event] right key pushed.')
            self.player_car.turn_right()

        if event.key == K_UP:
            print(f'[event] up key pushed.')
            self.player_car.turn_up()

        if event.key == K_DOWN:
            print(f'[event] down key pushed.')
            self.player_car.turn_down()

        if event.key == K_r:
            print(f'[event] `R` key pushed.')
            self.reset()

    def _deal_with_action(self, action):
        if action == CarControlAction.ACTION_TURN_LEFT:
            self.player_car.turn_left()
        elif action == CarControlAction.ACTION_TURN_RIGHT:
            self.player_car.turn_right()
        else:
            pass

    def _move_player_car(self):
        # move the object
        self.player_car.move()
        self.__deal_with_boarder_situation()

    def __deal_with_boarder_situation(self):
        if self.player_car.body_left < 0 or self.player_car.body_right > self.game_engine.map_width:
            self.player_car.rebound_horizontally()
        if self.player_car.body_top < 0 or self.player_car.body_bottom > self.game_engine.map_height:
            self.player_car.rebound_vertically()

    def reset(self):
        # TODO: fill with correct logic to reset the game
        self._init_game_engine()
        self._init_player_car()
        self._init_environment()
        self.game_status = GameStatus.Running

    def destroy(self):
        # TODO: fill with correct logic to destroy game
        self.game_status = GameStatus.Destroyed


def start_game():
    car_game_instance = CarGame()
    car_game_instance.run()
