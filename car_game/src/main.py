from core.game import start_game
from model.car_ai import CarAI


def main():
    print('welcome to car core')
    start_game(CarAI())


if __name__ == "__main__":
    main()
