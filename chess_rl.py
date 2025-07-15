import numpy as np
import random
from collections import defaultdict
import chess

class ChessEnv:
    def __init__(self):
        self.board = chess.Board()
        self.current_player = 1 #1 = White, -1 = Black

    def reset(self):
        self.board = chess.Board()
        self.current_player = 1
        return self.get_state()
    
    def get_state(self):
        return self.board.fen()
    
    def get_legal_moves(self):
        return self.board.legal_moves
    
    def step(self, move):
        action = move
        
