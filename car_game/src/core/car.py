from enum import Enum
import math
from typing import List
import numpy as np

from car_game.src.core.geometry import Point, Line
from car_game.src.core.geometry import utils
import car_game.src.config.game as GAME_SETTING
from car_game.src.core.enviroment import EnvironmentMap

PI = np.pi


class CarControlAction(Enum):
    ACTION_IDLE = 0
    ACTION_TURN_LEFT = 1
    ACTION_TURN_RIGHT = 2


class CarTerminal(Enum):
    Running = 0
    Failed = 1
    Success = 2

class Car:
    """
    direction: 行驶方向与x轴正方向夹角，初始值为0，范围[-pi, pi]，y轴正方向为 pi / 2
    v: 车速，初始值为0
    w: 角速度，初始值为0
    acc_v: 加速度，始终为0.2
    acc_w: 角加速度，Action=Right时 acc_w=0.1，Action=Left时 acc_w=-0.1
    position: 位置
    width: 宽度
    height: 高度

    get_left_front_point: 求汽车左前顶点坐标
    get_right_front_point: 求汽车右前顶点坐标
    get_left_behind_point: 求汽车左后顶点坐标
    get_right_behind_point: 求汽车右后顶点坐标

    """

    direction: float
    v: float
    w: float
    acc_v: float
    acc_w: float
    position: Point
    start_pos: Point
    width: int
    height: int

    observation: List[float]
    reward: float
    terminal: CarTerminal

    def __init__(self, start_pos: Point):
        self.start_pos = start_pos
        self.reset_car()

    def reset_car(self):
        self.direction = 0
        self.v = GAME_SETTING.GAME_CAR_V0
        self.w = 0
        self.acc_v = GAME_SETTING.GAME_CAR_V_ACC
        self.acc_w = 0
        self.position = Point(self.start_pos.x, self.start_pos.y)
        self.width = GAME_SETTING.GAME_CAR_WIDTH
        self.height = GAME_SETTING.GAME_CAR_HEIGHT

        self.observation = GAME_SETTING.INIT_OBSERVATION
        self.reward = 0
        self.terminal = CarTerminal.Running

    def receive_control(self, action: CarControlAction = CarControlAction.ACTION_IDLE):
        dt = GAME_SETTING.GAME_STEP_INTERVAL / 1000
        if action == CarControlAction.ACTION_TURN_LEFT:
            self.acc_w = 0 - GAME_SETTING.GAME_CAR_W_ACC
            self.acc_v = GAME_SETTING.GAME_CAR_V_ACC_LR
        elif action == CarControlAction.ACTION_TURN_RIGHT:
            self.acc_w = GAME_SETTING.GAME_CAR_W_ACC
            self.acc_v = GAME_SETTING.GAME_CAR_V_ACC_LR
        elif action == CarControlAction.ACTION_IDLE:
            self.acc_w = 0
            self.acc_v = GAME_SETTING.GAME_CAR_V_ACC

        # Auto-center if:
        #   1. IDLE, or
        #   2. LEFT when steering right, or
        #   3. RIGHT when steering left
        if self.w * self.acc_w <= 0:
            self.w = 0

        self.w = self.w + self.acc_w * dt
        self.direction = utils.normalized_direction(self.direction + self.w * dt)
        self.v = min(self.v + self.acc_v * dt, GAME_SETTING.GAME_CAR_MAX_V)

        v_x, v_y = self.v * math.cos(self.direction), self.v * math.sin(self.direction)
        self.position.x, self.position.y = self.position.x + v_x * dt, self.position.y + v_y * dt

    def calculate_observation_reward_terminal(self, env_map: EnvironmentMap):
        self.terminal = self._calculate_terminal(env_map)
        if self.terminal == CarTerminal.Failed:
            self.observation = self._calculate_observation(env_map)
            self.reward = -1
        elif self.terminal == CarTerminal.Success:
            self.observation = GAME_SETTING.INIT_OBSERVATION
            self.reward = GAME_SETTING.MAX_REWARD
        elif self.terminal == CarTerminal.Running:
            self.observation = self._calculate_observation(env_map)
            self.reward = self._calculate_reward(env_map)

        return self.observation, self.reward, self.terminal

    def calculate_observation_terminal(self, env_map: EnvironmentMap):
        self.terminal = self._calculate_terminal(env_map)
        if self.terminal == CarTerminal.Failed:
            self.observation = self._calculate_observation(env_map)
        elif self.terminal == CarTerminal.Success:
            self.observation = self._calculate_observation(env_map)
        elif self.terminal == CarTerminal.Running:
            self.observation = self._calculate_observation(env_map)

        return self.observation, self.terminal

    def calculate_terminal(self, env_map: EnvironmentMap):
        self.terminal = self._calculate_terminal(env_map)
        return self.terminal

    def _calculate_terminal(self, env_map: EnvironmentMap):
        if self._check_crash(env_map):
            return CarTerminal.Failed
        if self._check_success(env_map):
            return CarTerminal.Success
        return CarTerminal.Running


    def _calculate_dist_block(self, direction, env_map: EnvironmentMap):
        dist = GAME_SETTING.MAX_OBSERVATION
        for block in env_map.block_list:
            b_l_t = Point(block.position.x - block.size / 2, block.position.y - block.size / 2)
            b_l_b = Point(block.position.x - block.size / 2, block.position.y + block.size / 2)
            b_r_t = Point(block.position.x + block.size / 2, block.position.y - block.size / 2)
            b_r_b = Point(block.position.x + block.size / 2, block.position.y + block.size / 2)
            temp = utils.intersect_ray_line(self.position, direction, [b_l_t, b_l_b, b_r_b, b_r_t, b_l_t])
            if temp < dist:
                dist = temp
        return dist

    def _calculate_observation(self, env_map: EnvironmentMap):
        dirs = [self.direction - PI / 4,
                self.direction - PI / 6,
                self.direction,
                self.direction + PI / 6,
                self.direction + PI / 4]

        observation = []
        for direction in dirs:
            dist_left = utils.intersect_ray_line(self.position, direction, env_map.left_barrier_line)

            dist_right = utils.intersect_ray_line(self.position, direction, env_map.right_barrier_line)

            dist_block = self._calculate_dist_block(direction, env_map)

            observation.append(min(GAME_SETTING.MAX_OBSERVATION, dist_left, dist_right, dist_block))

        return observation

    def _calculate_reward(self, env_map: EnvironmentMap):
        dist = env_map.dist_to_destination(self.position)
        reward = (1 - dist / env_map.total_length) * GAME_SETTING.MAX_REWARD
        return reward

    def _check_crash(self, env_map: EnvironmentMap):
        l_f = self.get_left_front_point()
        r_f = self.get_right_front_point()
        l_b = self.get_left_behind_point()
        r_b = self.get_right_behind_point()

        for i in range(len(env_map.left_barrier_line) - 1):
            line = Line(env_map.left_barrier_line[i], env_map.left_barrier_line[i + 1])
            if utils.is_intersect(line, l_f, l_b, r_f, r_b):
                return True

        for i in range(len(env_map.right_barrier_line) - 1):
            line = Line(env_map.right_barrier_line[i], env_map.right_barrier_line[i + 1])
            if utils.is_intersect(line, l_f, l_b, r_f, r_b):
                return True

        for block in env_map.block_list:
            b_l_t = Point(block.position.x - block.size / 2, block.position.y - block.size / 2)
            b_l_b = Point(block.position.x - block.size / 2, block.position.y + block.size / 2)
            b_r_t = Point(block.position.x + block.size / 2, block.position.y - block.size / 2)
            b_r_b = Point(block.position.x + block.size / 2, block.position.y + block.size / 2)
            line_list = [Line(b_l_t, b_l_b), Line(b_l_t, b_r_t), Line(b_r_b, b_r_t), Line(b_r_b, b_l_b)]
            for line in line_list:
                if utils.is_intersect(line, l_f, l_b, r_f, r_b):
                    return True

        return False

    def _check_success(self, env_map: EnvironmentMap):
        l_f = self.get_left_front_point()
        r_f = self.get_right_front_point()
        l_b = self.get_left_behind_point()
        r_b = self.get_right_behind_point()

        if utils.is_intersect(env_map.destinationLine, l_f, l_b, r_f, r_b):
            return True
        return False

    def get_left_front_point(self):
        return self.position + utils.rotate(Point(self.height / 2, self.width / 2), self.direction)

    def get_right_front_point(self):
        return self.position + utils.rotate(Point(self.height / 2, 0 - self.width / 2), self.direction)

    def get_left_behind_point(self):
        return self.position + utils.rotate(Point(0 - self.height / 2, self.width / 2), self.direction)

    def get_right_behind_point(self):
        return self.position + utils.rotate(Point(0 - self.height / 2, 0 - self.width / 2), self.direction)

    def get_observation_pos(self):
        dirs = [self.direction - PI / 4,
                self.direction - PI / 6,
                self.direction,
                self.direction + PI / 6,
                self.direction + PI / 4]
        pos_list = []
        for i in range(len(dirs)):
            observation_x = round(math.cos(dirs[i]) * self.observation[i] + self.position.x)
            observation_y = round(math.sin(dirs[i]) * self.observation[i] + self.position.y)
            pos_list.append((observation_x, observation_y))
        return pos_list

    def output_car_info(self):
        print("pos: ", self.position.x, self.position.y)
        print("direction: ", self.direction)
        print("v: ", self.v)
        print("w: ", self.w)
        print("acc_v: ", self.acc_v)
        print("acc_w: ", self.acc_w)
        print("----------------------------------------")