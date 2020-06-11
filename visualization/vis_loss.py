import os
import pickle
import torch
import numpy as np
import math
from matplotlib import pyplot as plt

#### Please run in the bash, iteractive mode not capable in pycharm

LOSS_ROOT = os.path.join("logs", "loss.pkl")

if __name__ == "__main__":
    plt.figure(figsize=(8, 6), dpi=80)
    plt.ion()

    file_weights = open(LOSS_ROOT, "rb")
    loss_history = pickle.load(file_weights)
    print(len(loss_history))
    x = []
    y = []
    for epoch, loss in enumerate(loss_history):
        x.append(epoch + 1)
        y.append(loss)
        plt.xlim(1, 50 * math.ceil(epoch / 50))
        plt.plot(x, y, color='r')
        plt.pause(0.05)
    plt.ioff()
    plt.show()