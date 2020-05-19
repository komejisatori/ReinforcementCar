

class EnvironmentMap:
    """
    the environment map info in the game
    """
    pass


class EnvironmentPosition:
    """
    the position in the map
    """
    x: int
    y: int

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

