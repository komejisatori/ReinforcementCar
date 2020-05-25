from enum import Enum
import time

import car_game.src.config.resource as RESOURCE
import car_game.src.config.game as GAME_SETTING

from car_game.src.core.car import Car, CarControlAction, CarTerminal
from car_game.src.core.enviroment import EnvironmentMap
from car_game.src.core.geometry import Point
import pygame
import pygame.gfxdraw
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
        # img_icon = pygame.image.load(RESOURCE.IMAGE_ICON_FILE_PATH)
        # pygame.display.set_icon(img_icon)
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
            if self.game_status != GameStatus.Running:
                self.reset()

            if False:
                action = CarControlAction(GAME_SETTING.List[i])
            else:
                keys = pygame.key.get_pressed()
                left_key = keys[pygame.K_LEFT]
                right_key = keys[pygame.K_RIGHT]
                if left_key == right_key:
                    # Both pressed or both not pressed
                    action = CarControlAction.ACTION_IDLE
                elif left_key:
                    action = CarControlAction.ACTION_TURN_LEFT
                else:
                    action = CarControlAction.ACTION_TURN_RIGHT

            self.step(action=action, reward=0, training=True)

            # self.player_car.output_car_info()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == KEYDOWN:
                    pass
            self.render()
            pygame.time.delay(GAME_SETTING.GAME_STEP_INTERVAL)
            i = (i + 1) % len(GAME_SETTING.List)



    def step(self, action: CarControlAction, reward, training=True):
        """
        one step
        :param action:
        :param training:
        :return:
        """
        assert self.game_status == GameStatus.Running
        if not training:
            pass
        else:
            self.player_car.reward = reward
            self.player_car.receive_control(action)
            observation, terminal = self.player_car.calculate_observation_terminal(self.environment_map)
            if terminal == CarTerminal.Failed:
                self.game_status = GameStatus.Failed
            elif terminal == CarTerminal.Success:
                self.game_status = GameStatus.Success

            return observation, terminal



    def reset(self):
        self.player_car.reset_car()
        self.game_status = GameStatus.Running

    def destroy(self):
        self.game_status = GameStatus.Destroyed

    def render(self):
        self._render_background()
        self._render_environment(self.environment_map)
        self._render_cars(self.player_car)
        self._render_observations(self.player_car)
        self._render_reward_terminal(self.player_car)
        #self._render_player_car(self.player_car)
        pygame.display.flip()

    def _render_background(self):
        self.screen.fill(self.color_bg)

    def _render_environment(self, environment:EnvironmentMap, color=(0,0,0)):
        left_lines = [p.to_pair() for p in environment.left_barrier_line]
        right_lines = [p.to_pair() for p in environment.right_barrier_line]
        pygame.draw.aalines(self.screen, color, False, left_lines)
        pygame.draw.aalines(self.screen, color, False, right_lines)
        des_line = environment.destinationLine
        color_des = (255, 210, 0)
        pygame.draw.aaline(self.screen, color_des, des_line.p1.to_pair(), des_line.p2.to_pair())

    def _render_cars(self, car:Car, color=(0,0,0)):
        car_vertex_list = [car.get_left_front_point().to_pair(), car.get_right_front_point().to_pair(),
                           car.get_right_behind_point().to_pair(), car.get_left_behind_point().to_pair()]
        pygame.gfxdraw.aapolygon(self.screen, car_vertex_list, color)
        # pygame.draw.polygon(self.screen, color, car_vertex_list)
        pygame.gfxdraw.filled_polygon(self.screen, car_vertex_list, color)

    def _render_observations(self, car:Car, color=(0,137,167), radius = 2):
        observation_pos = car.get_observation_pos()
        for p in observation_pos:
            pygame.draw.circle(self.screen, color, p, radius)

    def _render_reward_terminal(self, car:Car):
        reward_terminal = f"reward: {car.reward:.2f} terminal: {car.terminal.value}"
        self.__draw_text(reward_terminal)

    def prepare(self):
        self.game_status = GameStatus.NotStarted
        self.__show_cover()
        if self.game_status == GameStatus.NotStarted:
            self.__prepare_left_barrier()
            self.__prepare_right_barrier()
            self.environment_map.build_destination_line()
            # TODO: draw obstacle objects
            self.game_status = GameStatus.Running
        # finish prepare, start to run

    def __show_cover(self):
        text_alpha = 1.0
        while True:
            enter_next_step = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_RETURN]:
                        self.game_status = GameStatus.Running
                    enter_next_step = True
            if enter_next_step:
                break
            # background
            self.screen.fill((0, 0, 0))
            img_cover = pygame.image.load(RESOURCE.IMAGE_COVER_FILE_PATH)
            img_cover = pygame.transform.scale(img_cover, (GAME_SETTING.GAME_SCREEN_WIDTH, GAME_SETTING.GAME_SCREEN_HEIGHT))
            self.screen.blit(img_cover, img_cover.get_rect())
            # illustration
            illustration_text = "press ENTER key to directly start, or press other keys to edit match track."
            text_alpha = text_alpha + 30
            if text_alpha > 255:
                text_alpha -= 255
            self.__draw_text(illustration_text, 24, color=(255, 255, 0, 255))
            pygame.display.flip()
            pygame.time.delay(GAME_SETTING.GAME_STEP_INTERVAL)

    def __prepare_left_barrier(self):
        # draw left barrier
        while True:
            enter_next_step = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_RETURN]:
                        enter_next_step = True
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    current_point = Point(pos[0], pos[1])
                    if event.button == pygame.BUTTON_LEFT:
                        self.environment_map.extend_left_barrier_line(current_point)
                    elif event.button == pygame.BUTTON_RIGHT:
                        self.environment_map.cut_left_barrier_line()
            if enter_next_step:
                break
            illustration_text = f"click left button to draw left barriers, right button to delete, enter to next."
            self.render_prepare_ui(illustration_text)
            pygame.time.delay(GAME_SETTING.GAME_STEP_INTERVAL)

    def __prepare_right_barrier(self):
        # draw right barrier
        while True:
            enter_next_step = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_RETURN]:
                        enter_next_step = True
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    current_point = Point(pos[0], pos[1])
                    if event.button == pygame.BUTTON_LEFT:
                        self.environment_map.extend_right_barrier_line(current_point)
                    elif event.button == pygame.BUTTON_RIGHT:
                        self.environment_map.cut_right_barrier_line()
            if enter_next_step:
                break
            illustration_text = f"click left button to draw right barriers, right button to delete, enter to next."
            self.render_prepare_ui(illustration_text)
            pygame.time.delay(GAME_SETTING.GAME_STEP_INTERVAL)

    def render_prepare_ui(self, illustration_text=""):
        # background
        self.screen.fill((255, 255, 0))
        # illustration
        self.__draw_text(illustration_text)
        # environment
        self._render_environment(self.environment_map)
        pygame.display.flip()

    def __draw_text(self, text='', font_size=18, top=2, left=0, color=(0, 0, 0)):
        font_obj = pygame.font.SysFont('arial', font_size)  # 通过字体文件获得字体对象
        illustration_surface_obj = font_obj.render(text, True, color)  # 配置要显示的文字
        illustration_rect_obj = illustration_surface_obj.get_rect()  # 获得要显示的对象的rect
        illustration_rect_obj.topleft = (top, left)  # 设置显示对象的坐标
        self.screen.blit(illustration_surface_obj, illustration_rect_obj)

def start_game():
    car_game_instance = CarGame()
    car_game_instance.prepare()
    car_game_instance.run()