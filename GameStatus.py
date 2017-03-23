from enum import Enum

from Singleton import *


class GameStage(Enum):
    BeforeFight = 1
    Fighting = 2
    AfterFight = 3
    Stopped = 4


class GameStatus(metaclass=Singleton):
    def __init__(self):
        self.game_stage = None
        self.current_level = None
        self.cards = []
        self.window = None
        self.y = 989.0
        self.use_Droid4X = False
