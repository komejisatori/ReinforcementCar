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

    def increase_right(self, value):
        self.right += value

    def increase_down(self, value):
        self.down += value

    def increase_left(self, value):
        self.increase_right(-value)

    def increase_up(self, value):
        self.increase_down(-value)

    def reverse_right(self):
        self.right = -self.right

    def reverse_down(self):
        self.down = -self.down


class CarAcceleration:
    # TODO: modify it to change the total speed of the game
    SAMPLE_ACCELERATION_VALUE = 5
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
    width: int
    height: int

    def __init__(self, position: EnvironmentPosition, width, height):
        self.velocity = CarVelocity.get_static_velocity()
        self.acceleration = CarAcceleration.get_zero_acceleration()
        self.position = position
        self.width = width
        self.height = height

    def receive_control(self, action: CarControlAction = CarControlAction.ACTION_NONE):
        if action == CarControlAction.ACTION_TURN_LEFT:
            self.turn_left()
        elif action == CarControlAction.ACTION_TURN_RIGHT:
            self.turn_right()
        else:
            pass

    def turn_left(self):
        # TODO: modify to fill real velocity change
        self.velocity.increase_left(CarAcceleration.SAMPLE_ACCELERATION_VALUE)

    def turn_right(self):
        # TODO: modify to fill real velocity change
        self.velocity.increase_right(CarAcceleration.SAMPLE_ACCELERATION_VALUE)

    def turn_up(self):
        # TODO: modify to fill real velocity change
        self.velocity.increase_up(CarAcceleration.SAMPLE_ACCELERATION_VALUE)

    def turn_down(self):
        # TODO: modify to fill real velocity change
        self.velocity.increase_down(CarAcceleration.SAMPLE_ACCELERATION_VALUE)

    def rebound_horizontally(self):
        self.velocity.reverse_right()

    def rebound_vertically(self):
        self.velocity.reverse_down()

    def move(self):
        self.position.x += self.velocity.right
        self.position.y += self.velocity.down

    @property
    def body_left(self):
        return self.position.x

    @property
    def body_right(self):
        return self.position.x + self.width

    @property
    def body_top(self):
        return self.position.y

    @property
    def body_bottom(self):
        return self.position.y + self.height