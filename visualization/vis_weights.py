import os
import pickle
import torch
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt

#### Please run in the bash, iteractive mode not capable in pycharm

WEIGHTS_ROOT = os.path.join("logs", "weights.pkl")

LAYERS = [4, 4, 3]
LAYER_NAMES = ['input', 'hidden.0', 'hidden.1', 'output']

if __name__ == "__main__":
    plt.figure(figsize=(8, 6), dpi=80)
    plt.ion()
    net = nx.Graph()
    input_node, output_node = 5, 3
    dimensions = [input_node] + LAYERS + [output_node]
    for layer_id, d in enumerate(dimensions):
        for i in range(d):
            net.add_node(str(layer_id) + '_' + str(i), label="Node_" + str(layer_id) + '_' + str(i),
                         pos=(layer_id * 100, i * 100 + (5 - d) * 50))
    for layer_id in range(len(dimensions) - 1):
        for i in range(dimensions[layer_id]):
            for j in range(dimensions[layer_id + 1]):
                net.add_edge(str(layer_id) + '_' + str(i), str(layer_id + 1) + '_' + str(j), weight=1)

    pos = nx.get_node_attributes(net, 'pos')
    plt.cla()
    nx.draw(net, pos,  node_color="steelblue", with_labels=False, node_size=200, edge_color="black",
            width=1, cmap=plt.cm.Dark2, edge_cmap=plt.cm.Blues)
    plt.text(380, 450, 'epoch: {}'.format(0), fontsize=20)
    plt.pause(0.2)

    file_weights = open(WEIGHTS_ROOT, "rb")
    weights_history = pickle.load(file_weights)
    print(len(weights_history))
    for epoch, weights in enumerate(weights_history):
        print(weights['output.weight'])
        for layer_id in range(len(LAYER_NAMES)):
            layer_weight = weights[LAYER_NAMES[layer_id] + '.weight'].numpy()
            layer_bias = weights[LAYER_NAMES[layer_id] + '.bias'].numpy()
            for i in range(dimensions[layer_id]):
                for j in range(dimensions[layer_id + 1]):
                    net[str(layer_id) + '_' + str(i)][str(layer_id + 1) + '_' + str(j)]['weight'] = layer_weight[j][i]
        width_list = [abs(d['weight']) * 20 for (u, v, d) in net.edges(data=True)]
        edge_color_list = ['green' if d['weight'] > 0 else 'red' for (u, v, d) in net.edges(data=True)]
        plt.cla()
        nx.draw(net, pos, node_color="steelblue", with_labels=False, node_size=200, edge_color=edge_color_list,
                width=width_list)
        plt.text(350, 450, 'Saving point: {}'.format((epoch + 1)), fontsize=10)
        plt.pause(0.2)
    plt.ioff()
    plt.show()