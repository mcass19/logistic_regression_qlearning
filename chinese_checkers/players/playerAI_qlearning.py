from chinese_checkers.board import Board
from chinese_checkers.players.player import Player

import numpy as np

class PlayerAIQLearning(Player):

    def __init__(self, id):
        super().__init__(id)
    