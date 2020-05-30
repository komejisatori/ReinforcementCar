# structure config
LAYERS = [4,4,3]

# training config
STEP_FRAME = 1
RANDOM_EPSILON = 1
RANDOM_EPSILON_DECAY = 0.9
RANDOM_EPSILON_MIN = 0.001
ACTION_NUMBER = 3
ACTIONS = ['IDLE','LEFT','RIGHT']
MEMORY = 1000
BATCH = 32
OBSERVE = 50
GAMMA = 0.9
SAVE_STEP = 100
DEMO_STEP = 10
DECAY_STEP = 50000
LR = 0.001
LR_MIN = 0.00001
LR_GAMMA = 0.1


