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
from car_game.src.model.car_ai import reward_system


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
        self.offset_x = 0
        self.offset_y = 0
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
        self._perspective_tracking(self.player_car.position)
        self._render_background()
        self._render_environment(self.environment_map)
        self._render_moving_blocks(self.environment_map)
        self._render_cars(self.player_car)
        self._render_cars(self.user_car, color=(255,0,0))
        self._render_observations(self.player_car)
        self._render_reward_terminal(self.player_car)
        pygame.display.flip()

    def _perspective_tracking(self, center_pos:Point):
        center_x = center_pos.x
        center_y = center_pos.y
        screen_width = GAME_SETTING.GAME_SCREEN_WIDTH
        screen_height = GAME_SETTING.GAME_SCREEN_HEIGHT
        map_width = GAME_SETTING.GAME_MAP_WIDTH
        map_height = GAME_SETTING.GAME_MAP_HEIGHT

        if screen_width >= map_width or center_x - screen_width/2 <= 0:
            self.offset_x = 0
        elif center_x + screen_width/2 >= map_width:
            self.offset_x = map_width - screen_width
        else:
            self.offset_x = center_x - screen_width/2

        if screen_height >= map_height or center_y - screen_height/2 <= 0:
            self.offset_y = 0
        elif center_y + screen_height/2 >= map_height:
            self.offset_y = map_height - screen_height
        else:
            self.offset_y = center_y - screen_height/2

        self.offset_x = round(self.offset_x)
        self.offset_y = round(self.offset_y)

    def _render_background(self):
        self.screen.fill(self.color_bg)

    def _render_environment(self, environment:EnvironmentMap, color=(0,0,0), tracking=True):
        left_lines = [p.to_pair() for p in environment.left_barrier_line]
        right_lines = [p.to_pair() for p in environment.right_barrier_line]
        if tracking:
            left_lines = [(p[0] - self.offset_x, p[1] - self.offset_y) for p in left_lines]
            right_lines = [(p[0] - self.offset_x, p[1] - self.offset_y) for p in right_lines]
        pygame.draw.aalines(self.screen, color, False, left_lines)
        pygame.draw.aalines(self.screen, color, False, right_lines)
        des_line = environment.destinationLine
        color_des = (255, 210, 0)
        des_line_p1 = des_line.p1.to_pair()
        des_line_p2 = des_line.p2.to_pair()
        if tracking:
            des_line_p1 = (des_line_p1[0] - self.offset_x, des_line_p1[1] - self.offset_y)
            des_line_p2 = (des_line_p2[0] - self.offset_x, des_line_p2[1] - self.offset_y)
        pygame.draw.aaline(self.screen, color_des, des_line_p1, des_line_p2)

    def _render_moving_blocks(self, environment:EnvironmentMap, block_color=(0,0,0), tracking=True):
        for block in environment.block_list:
            if tracking:
                pygame.draw.rect(self.screen, block_color, (block.position.x - block.size / 2 - self.offset_x, block.position.y - block.size / 2 - self.offset_y, block.size, block.size), 0)
            else:
                pygame.draw.rect(self.screen, block_color, (block.position.x - block.size / 2, block.position.y - block.size / 2, block.size, block.size), 0)

    def _render_cars(self, car:Car, color=(0,0,0), tracking=True):
        car_vertex_list = [car.get_left_front_point().to_pair(), car.get_right_front_point().to_pair(),
                           car.get_right_behind_point().to_pair(), car.get_left_behind_point().to_pair()]
        if tracking:
            car_vertex_list = [(p[0] - self.offset_x, p[1] - self.offset_y) for p in car_vertex_list]
        pygame.gfxdraw.aapolygon(self.screen, car_vertex_list, color)
        pygame.gfxdraw.filled_polygon(self.screen, car_vertex_list, color)

    def _render_observations(self, car:Car, color=(0,137,167), radius = 2, tracking=True):
        observation_pos = car.get_observation_pos()
        if tracking:
            observation_pos = [(p[0] - self.offset_x, p[1] - self.offset_y) for p in observation_pos]
        for p in observation_pos:
            pygame.draw.circle(self.screen, color, p, radius)

    def _render_reward_terminal(self, car:Car):
        reward_terminal = f"reward: {car.reward:.2f} terminal: {car.terminal.value}"
        self.__draw_text(reward_terminal)

    def prepare(self):
        self.game_status = GameStatus.NotStarted
        self.__show_cover()
        self.prepare_center = Point(GAME_SETTING.GAME_SCREEN_WIDTH/2,GAME_SETTING.GAME_SCREEN_HEIGHT/2)
        if self.game_status == GameStatus.NotStarted:
            self._perspective_tracking(self.prepare_center)
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
        screen_width = GAME_SETTING.GAME_SCREEN_WIDTH
        screen_height = GAME_SETTING.GAME_SCREEN_HEIGHT
        map_width = GAME_SETTING.GAME_MAP_WIDTH
        map_height = GAME_SETTING.GAME_MAP_HEIGHT
        while True:
            enter_next_step = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_RETURN]:
                        enter_next_step = True
                    elif event.key == pygame.K_LEFT:
                        if self.prepare_center.x >= screen_width / 2:
                            self.prepare_center.x -= 20
                            self._perspective_tracking(self.prepare_center)
                            print("left")
                            print(self.prepare_center.x, self.prepare_center.y)
                    elif event.key == pygame.K_RIGHT:
                        if self.prepare_center.x <= map_width - screen_width / 2:
                            self.prepare_center.x += 20
                            self._perspective_tracking(self.prepare_center)
                    elif event.key == pygame.K_UP:
                        if self.prepare_center.y >= screen_height / 2:
                            self.prepare_center.y -= 20
                            self._perspective_tracking(self.prepare_center)
                    elif event.key == pygame.K_DOWN:
                        if self.prepare_center.y <= map_height - screen_height / 2:
                            self.prepare_center.y += 20
                            self._perspective_tracking(self.prepare_center)
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    current_point = Point(pos[0] + self.offset_x, pos[1] + self.offset_y)
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
        screen_width = GAME_SETTING.GAME_SCREEN_WIDTH
        screen_height = GAME_SETTING.GAME_SCREEN_HEIGHT
        map_width = GAME_SETTING.GAME_MAP_WIDTH
        map_height = GAME_SETTING.GAME_MAP_HEIGHT
        while True:
            enter_next_step = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_RETURN]:
                        enter_next_step = True
                    elif event.key == pygame.K_LEFT:
                        if self.prepare_center.x >= screen_width / 2:
                            self.prepare_center.x -= 20
                            self._perspective_tracking(self.prepare_center)
                    elif event.key == pygame.K_RIGHT:
                        if self.prepare_center.x <= map_width - screen_width / 2:
                            self.prepare_center.x += 20
                            self._perspective_tracking(self.prepare_center)
                    elif event.key == pygame.K_UP:
                        if self.prepare_center.y >= screen_height / 2:
                            self.prepare_center.y -= 20
                            self._perspective_tracking(self.prepare_center)
                    elif event.key == pygame.K_DOWN:
                        if self.prepare_center.y <= map_height - screen_height / 2:
                            self.prepare_center.y += 20
                            self._perspective_tracking(self.prepare_center)
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    current_point = Point(pos[0] + self.offset_x, pos[1] + self.offset_y)
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

def start_game(ai_car):
    car_game_instance = CarGame(ai_car)
    car_game_instance.prepare()
    car_game_instance.run()
