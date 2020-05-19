import pygame
import sys
from pygame.locals import *

import config.resource as RESOURCE
import config.game as GAME_SETTING

from core.car import Car
from core.enviroment import EnvironmentPosition


class CarGame:

    def __init__(self):
        self._init_setting()
        self._init_player_car()

    def _init_setting(self):
        # 初始化pygame
        pygame.init()

        size = width, height = GAME_SETTING.GAME_SCREEN_WIDTH, GAME_SETTING.GAME_SCREEN_HEIGHT
        self.speed = [-2, 1]

        # 背景设置，全白
        self.color_bg = (255, 255, 255)
        self.img_bg = pygame.image.load(RESOURCE.IMAGE_COVER_FILE_PATH)

        # 创建指定大小的窗口 Surface对象
        self.screen = pygame.display.set_mode(size)
        # 设置窗口标题
        pygame.display.set_caption(GAME_SETTING.GAME_TITLE)
        img_icon = pygame.image.load(RESOURCE.IMAGE_ICON_FILE_PATH)
        pygame.display.set_icon(img_icon)

        img_car = pygame.image.load(RESOURCE.IMAGE_CAR_FILE_PATH)
        self.img_car = pygame.transform.scale(img_car, (GAME_SETTING.GAME_CAR_WIDTH, GAME_SETTING.GAME_CAR_HEIGHT))

        # 获得图像的位置矩形
        self.position = img_car.get_rect()

    def _init_player_car(self):
        self.start_point = EnvironmentPosition(20, 20)
        self.player_car = Car(self.start_point)

    def run(self):

        # Main Loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == KEYDOWN:

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

            # TODO: move the object
            self.position = self.position.move(self.player_car.velocity.to_pygame_speed())

            # fill bg
            self.screen.fill(self.color_bg)
            # 更新图像
            self.screen.blit(self.img_car, self.position)
            # 更新界面
            pygame.display.flip()
            # 延时
            pygame.time.delay(50)


def start_game():
    car_game_instance = CarGame()
    car_game_instance.run()
