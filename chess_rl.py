import numpy as np
import random
from collections import defaultdict
import chess

class ChessEnv:
    def __init__(self):
        self.board = chess.Board(chess.STARTING_FEN)

    def reset(self):
        self.board = chess.Board(chess.STARTING_FEN)
        return self.get_state()
    
    def get_state(self):
        return self.board
    
    def get_legal_moves(self):
        return self.board.legal_moves
    
    def step(self, move):
        if isinstance(move, str):
            self.board.push_san(move)
        else:
            self.board.push(move)

        if self.board.is_checkmate():
            if self.board.turn:
                reward = -1
                return self.get_state(), reward, True
            else:
                reward = 1
                return self.get_state(), reward, True
        
        if self.board.is_stalemate() or self.board.is_repetition() or self.board.is_fifty_moves():
            reward = 0
            return self.get_state(), reward, True

        return self.get_state(), 0, False
    
class MoveEncoder:
    def __init__(self):
        # Generate all possible legal moves from all positions
        self.move_to_index = {}
        self.index_to_move = {}
        
        index = 0
        # Iterate through all possible from-to square combinations
        for from_square in range(64):
            for to_square in range(64):
                if from_square == to_square:
                    continue
                
                # Regular move (no promotion)
                move = chess.Move(from_square, to_square)
                self.move_to_index[move] = index
                self.index_to_move[index] = move
                index += 1
                
                # Promotion moves (only for moves to the back rank)
                to_rank = chess.square_rank(to_square)
                if to_rank == 0 or to_rank == 7:  # Back ranks
                    for promotion in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
                        promo_move = chess.Move(from_square, to_square, promotion=promotion)
                        self.move_to_index[promo_move] = index
                        self.index_to_move[index] = promo_move
                        index += 1
        
        self.num_actions = index
        print(f"Total possible moves: {self.num_actions}")
    
    def encode(self, move):
        """Convert a chess.Move to an integer index"""
        return self.move_to_index.get(move, None)
    
    def decode(self, index):
        """Convert an integer index back to a chess.Move"""
        return self.index_to_move.get(index, None)
    
    def encode_legal_moves(self, board):
        """Get indices of all legal moves for current position"""
        return [self.move_to_index[move] for move in board.legal_moves 
                if move in self.move_to_index]

