import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import torch.nn.init as init
from config import LAYERS


class RLNetwork(nn.Module):

    def __init__(self, 
    layer_config, 
    input_node=5, 
    output_node=3):
        super(RLNetwork, self).__init__()
        self.input_node = input_node
        self.output_node = output_node
        self.layer_config = layer_config
        self.input = nn.Linear(input_node, self.layer_config[0])
        self.hidden = []
        for i in range(len(self.layer_config) - 1):
            self.hidden.append(nn.Linear(self.layer_config[i], self.layer_config[i+1]))
        self.hidden = nn.Sequential(*self.hidden)
        self.output = nn.Linear(self.layer_config[-1], output_node)
        self.weight_init()

    def weight_init(self, mode='normal'):
        initializer = normal_init
        initializer(self.input)
        initializer(self.output)
        for block in self.hidden:
            initializer(block)

    
    def forward(self, x):
        x = self.input(x)
        x = self.hidden(x)
        x = F.relu(x)
        x = self.output(x)
        #x = F.relu(x)
        return x




def eval_step(model, status):
    status = Variable(torch.from_numpy(np.asarray(status).astype(np.float32)))
    model.eval()
    with torch.no_grad():
        action = model(status)
    return action

def train_step(model, s_batch, a_batch, y_batch, optimizer, loss_func):
    model.train()

    s_batch = Variable(torch.from_numpy(np.asarray(s_batch).astype(np.float32)))
    a_batch = torch.LongTensor(a_batch)
    y_batch = Variable(torch.from_numpy(np.asarray(y_batch).astype(np.float32)))
    action = model(s_batch).gather(dim=1, index=a_batch)
    loss = loss_func(action, y_batch)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss

def normal_init(m):
    if isinstance(m, (nn.Linear, nn.Conv2d)):
        init.normal_(m.weight, 0, 0.02)
        if m.bias is not None:
            m.bias.data.fill_(0)
    elif isinstance(m, (nn.BatchNorm1d, nn.BatchNorm2d)):
        m.weight.data.fill_(1)
        if m.bias is not None:
            m.bias.data.fill_(0)

if __name__ == '__main__':
    print('test net')
    layer_config = LAYERS
    net = RLNetwork(LAYERS)
    print(net)