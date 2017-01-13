from enum import Enum, auto
from Singleton import *


class GameStage(Enum):
    BeforeFight = auto()
    Fighting = auto()
    AfterFight = auto()


class GameStatus(metaclass=Singleton):
    def __init__(self):
        self.game_stage = None
        self.current_level = None
        self.cards = []
        self.window = None
