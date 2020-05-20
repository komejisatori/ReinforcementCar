
## Install Dependency
install `pygame` by `pip` tools:
```shell script
pip install -r requirements
```

## Run Demo
Start the game by:
```shell script
python src/main.py
```

## Core Class Illustration

- `CarGame`: the main class of the game
- `CarGameEngine`: responsible for dealing with the screen rendering
- `Car`: used to describe a single player car, including its velocity and position, etc
- `Environment`: used to describe the game environment, including the barriers and other information


## TODOs

- [ ] Add Barriers in the Environment
- [ ] Fill logic when the player car hits the barriers.
- [ ] Fill logic of Observation
- [ ] Fill logic of Reward