"""
training pipeline
"""
import os
import torch
import math
import torch.nn as nn
from model.network import RLNetwork, eval_step, train_step
from car_game.src.core.game import CarGame
from collections import deque
from model.config import *
import random
import pygame
import argparse
import car_game.src.config.game as GAME_SETTING
from car_game.src.core.car import CarControlAction
from car_game.src.config.game import MAX_OBSERVATION
import pickle, copy

def main(args):
    '''
    if os.path.exists('model.pt'):
        print('load exist model')
        main_model = torch.load('model.pt')
        target_model = torch.load('model.pt')
    else:
    '''
    lr = LR
    epsilon = RANDOM_EPSILON
    weights_history = []
    loss_history = []
    if args.resume:
        print('[train] from exist model')
        lr = lr * 0.1
        epsilon = RANDOM_EPSILON_MIN

        # reset logs
        try:
            with open(os.path.join("logs", "weights.pkl"), "rb") as file_weights:
                weights_history = pickle.load(file_weights)
                file_weights.close()
        except:
            print("Valid weights history files do not exists")
        try:
            with open(os.path.join("logs", "loss.pkl"), "rb") as file_loss:
                loss_history = pickle.load(file_weights)
                file_loss.close()
        except:
            print("Valid loss history files do not exists")

        main_model = torch.load(os.path.join('model', 'model.pt'))
        target_model = torch.load(os.path.join('model', 'model.pt'))
    else:
        main_model = RLNetwork(LAYERS)
        target_model = RLNetwork(LAYERS)

    optimizer = torch.optim.Adam(main_model.parameters(), lr=lr)
    loss_func = nn.MSELoss()
    game = CarGame()
    game.prepare()
    frame = 0
    D = deque()
    reward = 0

    observation, terminal = game.step(0, reward=reward, training=True)

    while True:
        game.render()
        pygame.time.delay(GAME_SETTING.GAME_STEP_INTERVAL)
        #observation, reward, terminal = game.step(0, training=True)
        if frame % STEP_FRAME == 0:
            #print('[train] step on frame {}'.format(frame))
            if random.random() < epsilon:
                action = random.randrange(ACTION_NUMBER)
                print('[train] random action {}'.format(ACTIONS[action]))
            else:
                action = torch.argmax(eval_step(main_model,observation)).item()
                #print('[train] action {}'.format(ACTIONS[action]))
        else:
            #pass
            action = 0
            #print('[train] pass frame {}'.format(frame))

        observation_old = observation
        reward_old = reward
        terminal_old = terminal
        car_action = CarControlAction.ACTION_IDLE
        if action == 0:
            car_action = CarControlAction.ACTION_IDLE
        if action == 1:
            car_action = CarControlAction.ACTION_TURN_LEFT
        if action == 2:
            car_action = CarControlAction.ACTION_TURN_RIGHT
        observation, terminal = game.step(car_action, reward=reward, training=True)
        if terminal.value != 0:
            #print('[train] game end')
            game.reset()

        reward = reward_system(observation, terminal)

        #if distance2 > 0.7:
        #    reward = -1

        D.append((observation_old, action, reward, observation, terminal))
        if len(D) > MEMORY:
            D.popleft()
        if frame >= OBSERVE:
            minibatch = random.sample(D, BATCH)

            s1_batch = []
            a_batch = []
            for i in range(len(minibatch)):
                s1_batch.append(minibatch[i][3])
                a_batch.append([minibatch[i][1]])

            y, _ = torch.max(eval_step(target_model, s1_batch), dim=1)
            y_batch = []
            s_batch = []
            for i in range(len(minibatch)):
                terminal = minibatch[i][-1]
                s_batch.append(minibatch[i][0])
                if terminal.value != 0:
                    y_batch.append([minibatch[i][2]])
                else:
                    y_batch.append([minibatch[i][2] + GAMMA * y[i].item()])
            loss = train_step(main_model, s_batch, a_batch, y_batch, optimizer, loss_func)
            print('[train] loss: {}'.format(loss.item()))
            if frame % SAVE_STEP == 0:
                if epsilon > RANDOM_EPSILON_MIN:
                    epsilon *= RANDOM_EPSILON_DECAY
                    print('[train] epsilon {}'.format(epsilon))
                state_dict = main_model.state_dict()
                # save history
                weights_history.append(copy.deepcopy(state_dict))
                pickle.dump(weights_history, open(os.path.join("logs", "weights.pkl"), "wb"))
                loss_history.append(loss.item())
                pickle.dump(weights_history, open(os.path.join("logs", "loss.pkl"), "wb"))
                torch.save(main_model, 'model.pt')
            if frame % DECAY_STEP == 0 and frame != 0:
                if lr > LR_MIN:
                    lr = lr * LR_GAMMA
                    for param_group in optimizer.param_groups:
                        param_group["lr"] = lr

        frame += 1

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

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--resume', action='store_true', default=False)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    main(args)

