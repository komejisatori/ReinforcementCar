from enum import Enum
import time

import config.resource as RESOURCE
import config.game as GAME_SETTING

from core.car import Car, CarControlAction, CarTerminal
from core.enviroment import EnvironmentMap
from core.geometry import Point
import pygame
import pygame.gfxdraw
from pygame.locals import *
from model.car_ai import reward_system


class GameStatus(Enum):
    NotStarted = 0
    Running = 1
    ModelWin = 2
    UserWin = 3
    Destroyed = 4


class CarGame:
    # game_engine: CarGameEngine

    # 模型驾驶的车
    player_car: Car
    # 用户手动控制的车
    user_car: Car

    environment_map: EnvironmentMap
    game_status: GameStatus

    def __init__(self, ai_car=None):
        self.game_status = GameStatus.Running
        self._init_game()
        self._init_player_car()
        self._init_user_car()
        self._init_environment_map()
        self._init_render()
        self.ai_car = ai_car

    def _init_player_car(self):
        self.player_car = Car(Point(GAME_SETTING.GAME_PLAYER_CAR_START_POSX, GAME_SETTING.GAME_PLAYER_CAR_START_POSY))

    def _init_user_car(self):
        self.user_car = Car(Point(GAME_SETTING.GAME_USER_CAR_START_POSX, GAME_SETTING.GAME_USER_CAR_START_POSY))

    def _init_environment_map(self):
        self.environment_map = EnvironmentMap()
        # create moving block
        self.environment_map.create_moving_block(Point(50, 400), Point(150, 450))
        self.environment_map.create_moving_block(Point(130, 330), Point(155, 350))

    def _init_game(self):
        pygame.init()
        # img_icon = pygame.image.load(RESOURCE.IMAGE_ICON_FILE_PATH)
        # pygame.display.set_icon(img_icon)
        pygame.display.set_caption(GAME_SETTING.GAME_TITLE)

    def _init_render(self):
        self.map_width, self.map_height = GAME_SETTING.GAME_SCREEN_WIDTH, GAME_SETTING.GAME_SCREEN_HEIGHT
        self.map_size = self.map_width, self.map_height
        self.screen = pygame.display.set_mode(self.map_size)
        self.color_bg = (255, 255, 255)

    def run(self):
        # Main Loop
        j = 0
        reward = 0.0
        observation, terminal = self.step(CarControlAction.ACTION_IDLE, reward=0.0, training=True)
        while True:
            assert self.game_status == GameStatus.Running

            self.render()
            pygame.time.delay(GAME_SETTING.GAME_STEP_INTERVAL)

            player_car_action = CarControlAction.ACTION_IDLE
            action_num = self.ai_car.step(observation)
            if action_num == 0:
                player_car_action = CarControlAction.ACTION_IDLE
            if action_num == 1:
                player_car_action = CarControlAction.ACTION_TURN_LEFT
            if action_num == 2:
                player_car_action = CarControlAction.ACTION_TURN_RIGHT
            observation, terminal = self.step(action=player_car_action, reward=reward, training=True)
            reward = reward_system(observation, terminal)

            keys = pygame.key.get_pressed()
            left_key = keys[pygame.K_LEFT]
            right_key = keys[pygame.K_RIGHT]
            user_car_action = CarControlAction.ACTION_IDLE
            if left_key == right_key:
                # Both pressed or both not pressed
                user_car_action = CarControlAction.ACTION_IDLE
            elif left_key:
                user_car_action = CarControlAction.ACTION_TURN_LEFT
            else:
                user_car_action = CarControlAction.ACTION_TURN_RIGHT
            self.control_user_car(action=user_car_action)

            j += 1
            self.environment_map.update_moving_block(j * GAME_SETTING.GAME_STEP_INTERVAL / 1000.0)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == KEYDOWN:
                    pass

    def step(self, action: CarControlAction, reward, training=True):
        """
        one step
        :param action:
        :param reward:
        :param training:
        :return:
        """

        self.player_car.reward = reward
        self.player_car.receive_control(action)
        observation, terminal = self.player_car.calculate_observation_terminal(self.environment_map)
        if terminal == CarTerminal.Failed:
            self.player_car.reset_car()
        elif terminal == CarTerminal.Success and self.game_status == GameStatus.Running:
            self.game_status = GameStatus.ModelWin

        return observation, terminal

    def control_user_car(self, action: CarControlAction):
        self.user_car.receive_control(action)
        terminal = self.user_car.calculate_terminal(self.environment_map)
        if terminal == CarTerminal.Failed:
            self.user_car.reset_car()
        elif terminal == CarTerminal.Success and self.game_status == GameStatus.Running:
            self.game_status = GameStatus.UserWin

    def reset(self):
        self.player_car.reset_car()
        self.user_car.reset_car()
        self.game_status = GameStatus.Running

    def destroy(self):
        self.game_status = GameStatus.Destroyed

    def render(self):
        self._render_background()
        self._render_environment(self.environment_map)
        self._render_moving_blocks(self.environment_map)
        self._render_cars(self.player_car)
        self._render_cars(self.user_car, color=(255,0,0))
        self._render_observations(self.player_car)
        self._render_reward_terminal(self.player_car)
        pygame.display.flip()

    def _render_background(self):
        self.screen.fill(self.color_bg)

    def _render_environment(self, environment:EnvironmentMap, car_color=(0,0,0)):
        left_lines = [p.to_pair() for p in environment.left_barrier_line]
        right_lines = [p.to_pair() for p in environment.right_barrier_line]
        pygame.draw.aalines(self.screen, car_color, False, left_lines)
        pygame.draw.aalines(self.screen, car_color, False, right_lines)
        des_line = environment.destinationLine
        color_des = (255, 210, 0)
        pygame.draw.aaline(self.screen, color_des, des_line.p1.to_pair(), des_line.p2.to_pair())

    def _render_moving_blocks(self, environment:EnvironmentMap, block_color=(0,0,0)):
        for block in environment.block_list:
            pygame.draw.rect(self.screen, block_color, (block.position.x - block.size / 2, block.position.y - block.size / 2, block.size, block.size), 0)

    def _render_cars(self, car:Car, color=(0,0,0)):
        car_vertex_list = [car.get_left_front_point().to_pair(), car.get_right_front_point().to_pair(),
                           car.get_right_behind_point().to_pair(), car.get_left_behind_point().to_pair()]
        pygame.gfxdraw.aapolygon(self.screen, car_vertex_list, color)
        pygame.gfxdraw.filled_polygon(self.screen, car_vertex_list, color)

    def _render_observations(self, car:Car, color=(0,137,167), radius = 2):
        observation_pos = car.get_observation_pos()
        for p in observation_pos:
            pygame.draw.circle(self.screen, color, p, radius)

    def _render_reward_terminal(self, car:Car):
        font_obj = pygame.font.SysFont('arial', 18)  # 通过字体文件获得字体对象

        reward_terminal = f"reward: {car.reward:.2f} terminal: {car.terminal.value}"
        reward_surface_obj = font_obj.render(reward_terminal, True, (0,0,0))  # 配置要显示的文字

        reward_rect_obj = reward_surface_obj.get_rect()  # 获得要显示的对象的rect

        reward_rect_obj.topleft = (2, 0)  # 设置显示对象的坐标

        self.screen.blit(reward_surface_obj, reward_rect_obj)


def start_game(ai_car):
    car_game_instance = CarGame(ai_car)
    car_game_instance.run()
