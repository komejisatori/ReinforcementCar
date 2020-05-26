import torch
from torch.autograd import Variable
import numpy as np

from model.train import reward_system
from car_game.src.core.game import CarGame
from car_game.src.core.car import CarControlAction
from model.config import *
import pygame
import car_game.src.config.game as GAME_SETTING

class CarAI():
    def __init__(self, model_path='./model.pt'):
        self.model_path = model_path
        self.model_instance = torch.load(self.model_path)
        self.model_instance.eval()

    def step(self, observation):
        observation = Variable(torch.from_numpy(np.asarray(observation).astype(np.float32)))
        with torch.no_grad():
            act = torch.argmax(self.model_instance(observation))
        return act

if __name__ == '__main__':
    AI = CarAI(model_path='./model.pt')
    game = CarGame()
    game.prepare()
    frame = 0
    reward = 0
    observation, terminal = game.step(0, reward=reward, training=True)
    while True:
        game.render()
        pygame.time.delay(GAME_SETTING.GAME_STEP_INTERVAL)
        if frame % STEP_FRAME == 0:
            action = AI.step(observation)
            car_action = CarControlAction.ACTION_IDLE
            if action == 0:
                car_action = CarControlAction.ACTION_IDLE
            if action == 1:
                car_action = CarControlAction.ACTION_TURN_LEFT
            if action == 2:
                car_action = CarControlAction.ACTION_TURN_RIGHT

            observation, terminal = game.step(car_action, reward=reward, training=True)
            reward = reward_system(observation, terminal)
        if terminal.value != 0:
            game.reset()
        frame += 1