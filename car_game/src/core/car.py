from core.enviroment import EnvironmentPosition


class CarVelocity:
    """
    the instant velocity for a car
    """
    right: float
    down: float

    def __init__(self, right: float = 0, down: float = 0):
        self.right = right
        self.down = down

    @staticmethod
    def get_static_velocity():
        return CarVelocity()

    def to_pygame_speed(self):
        return [self.right, self.down]


class CarAcceleration:
    """
    the instant acceleration for a car
    """
    left: float
    right: float
    up: float
    down: float

    def __init__(self, left: float = 0, right: float = 0, up: float = 0, down: float = 0):
        self.left = left
        self.right = right
        self.up = up
        self.down = down

    @staticmethod
    def get_zero_acceleration():
        return CarAcceleration()


class CarControlAction:
    ACTION_NONE = 0
    ACTION_TURN_LEFT = 1
    ACTION_TURN_RIGHT = 2


class Car:
    """
    the protagonist in the game
    """

    velocity: CarVelocity
    acceleration: CarAcceleration
    position: EnvironmentPosition

    def __init__(self, position: EnvironmentPosition):
        self.velocity = CarVelocity.get_static_velocity()
        self.acceleration = CarAcceleration.get_zero_acceleration()
        self.position = position

    def receive_control(self, action: CarControlAction = CarControlAction.ACTION_NONE):
        if action == CarControlAction.ACTION_TURN_LEFT:
            self.turn_left()
        elif action == CarControlAction.ACTION_TURN_RIGHT:
            self.turn_right()
        else:
            pass

    def turn_left(self):
        # TODO: modify to fill real velocity change
        self.velocity.right -= 2

    def turn_right(self):
        # TODO: modify to fill real velocity change
        self.velocity.right += 2

    def turn_up(self):
        # TODO: modify to fill real velocity change
        self.velocity.down -= 2

    def turn_down(self):
        # TODO: modify to fill real velocity change
        self.velocity.down += 2
