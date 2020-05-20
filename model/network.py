import torch
import torch.nn as nn
import torch.nn.funtional as F
from .config import LAYERS

class RLNetwork(nn.Module):

    def __init__(self, 
    layer_config, 
    input_node=5, 
    output_node=3):
        self.input_node = input_node
        self.output_node = output_node
        self.layer_config = layer_config
        self.input = nn.Linear(input_node, self.layer_config[0])
        self.hidden = []
        for i in range(len(self.layer_config) - 1):
            self.hidden.append(nn.Linear(self.layer_config[i-1], self.layer_config[i]))
        self.hidden = nn.Sequential(*self.hidden)
        self.output = nn.Linear(self.layer_config[-1], output_node)
    
    def forward(self, x):
        x = self.input(x)
        x = self.hidden(x)
        x = self.output(x)
        x = F.softmax(x, dim=1)
        return x

if __name__ == '__main__':
    print('test net')
    layer_config = LAYERS
    net = RLNetwork(LAYERS)
    print(net)