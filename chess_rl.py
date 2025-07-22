import numpy as np
import random
from collections import defaultdict
import chess

class ChessEnv:
    def __init__(self):
        self.board = chess.Board(chess.STARTING_FEN)
        #self.current_player = 1 #1 = White, -1 = Black

    def reset(self):
        self.board = chess.Board(chess.STARTING_FEN)
        #self.current_player = 1
        return self.get_state()
    
    def get_state(self):
        return self.board.fen()
    
    def get_legal_moves(self):
        return self.board.legal_moves
    
    def step(self, move):
        self.board.push_san(move)

        if self.board.is_checkmate:
            if self.board.turn:
                reward = 1
                return self.get_state(), reward, True
            else:
                reward = -1
                return self.get_state(), reward, True
        
        if self.board.is_stalemate or self.board.is_repetition or self.board.is_fifty_moves:
            reward = 0
            return self.get_state(), reward, True

