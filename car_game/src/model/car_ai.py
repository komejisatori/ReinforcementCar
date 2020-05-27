import torch
from torch.autograd import Variable
import numpy as np


import os

BASE_DIR = os.path.join(os.path.dirname(__file__))
DEFAULT_MODEL_PATH = os.path.join(BASE_DIR, "model_best.pt")


class CarAI():
    def __init__(self, model_path=DEFAULT_MODEL_PATH):
        self.model_path = model_path
        self.model_instance = torch.load(self.model_path)
        self.model_instance.eval()

    def step(self, observation):
        observation = Variable(torch.from_numpy(np.asarray(observation).astype(np.float32)))
        with torch.no_grad():
            act = torch.argmax(self.model_instance(observation))
        return act


def reward_system(observation, terminal):
    distance1 = max(observation[1], observation[3]) / (observation[1] + observation[3])
    distance2 = max(observation[0], observation[4]) / (observation[0] + observation[4])
    distance3 = observation[2]
    reward = 0
    if terminal.value == 0:
        reward = 0
    if distance2 > 0.75:
        reward = -0.5
    if distance3 < 20:
        reward = -0.5
    if terminal.value == 1:
        reward = -1
    if terminal.value == 2:
        reward = 1
    return reward
