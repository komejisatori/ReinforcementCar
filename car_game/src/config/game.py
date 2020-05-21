
# Game Setting

# Basic Setting
GAME_TITLE = 'Reinforcement Car'
GAME_STEP_INTERVAL = 50


# Screen Setting
GAME_SCREEN_WIDTH = 640
GAME_SCREEN_HEIGHT = 480


# Audio Setting


# Car Setting
GAME_CAR_WIDTH = 10
GAME_CAR_HEIGHT = 20

GAME_CAR_START_POSX = 20
GAME_CAR_START_POSY = 440

GAME_CAR_V0 = 30
GAME_CAR_V_ACC = 10
GAME_CAR_V_ACC_LR = 8
GAME_CAR_MAX_V = 300

GAME_CAR_W_ACC = 2

INIT_OBSERVATION = [-1, -1, -1, -1, -1]
MAX_REWARD = 100
MAX_OBSERVATION = 80

# Map
BARRIER_LEFT_LINE = [(30, 410), (70, 410), (110, 380), (130, 300)]
BARRIER_RIGHT_LINE = [(30, 470), (70, 470), (110, 440), (150, 400), (170, 300)]

# Test
List = [0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]