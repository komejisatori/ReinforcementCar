import pygame
import sys
from pygame.locals import *

import config.resource as RESOURCE
import config.game as GAME_SETTING

from core.car import Car, CarControlAction
from core.enviroment import EnvironmentPosition

from core.observation import Observation, Reward



class CarGame:

    def __init__(self):
        self._init_setting()
        self._init_player_car()

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
        self.color_bg = (255, 255, 255)

        # player car
        self.img_car = pygame.image.load(RESOURCE.IMAGE_CAR_FILE_PATH)
        self.img_car = pygame.transform.scale(self.img_car, (GAME_SETTING.GAME_CAR_WIDTH, GAME_SETTING.GAME_CAR_HEIGHT))

        # 获得图像的位置矩形
        self.position = self.img_car.get_rect()

    def _init_player_car(self):
        self.start_point = EnvironmentPosition(20, 20)
        self.player_car = Car(self.start_point)

    def run(self):

        # Main Loop
        while True:
            self.step(action=CarControlAction.ACTION_NONE, training=False)

    def step(self, action: CarControlAction, training=True):
        """
        game forward
        :param action:
        :param training:
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == KEYDOWN:
                self._deal_with_key_down(event)

        self._move_player_car()
        self.render()

        return self._get_observation(), self._get_reward(), self._get_terminal()

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

    def _move_player_car(self):
        # move the object
        self.position = self.position.move(self.player_car.velocity.to_pygame_speed())
        self.__deal_with_boarder_situation()

    def render(self):
        # fill bg
        self.screen.fill(self.color_bg)
        # 更新图像
        self.screen.blit(self.img_car, self.position)
        # 更新界面
        pygame.display.flip()
        # 延时
        pygame.time.delay(GAME_SETTING.GAME_STEP_INTERVAL)

    def __deal_with_boarder_situation(self):
        if self.position.left < 0 or self.position.right > self.map_width:
            self.player_car.rebound_horizontally()
        if self.position.top < 0 or self.position.bottom > self.map_height:
            self.player_car.rebound_vertically()

    def _get_observation(self):
        # TODO: fill with correct logic
        return Observation()

    def _get_reward(self):
        # TODO: fill with correct logic
        return Reward()

    def _get_terminal(self):
        # TODO: fill with correct logic
        return 0

    def reset(self):
        # TODO: fill with correct logic to reset the game
        self._init_setting()
        self._init_player_car()

    def destroy(self):
        # TODO: fill with correct logic to destroy game
        pass


def start_game():
    car_game_instance = CarGame()
    car_game_instance.run()
