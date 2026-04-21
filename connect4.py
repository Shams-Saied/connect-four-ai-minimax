import numpy as np
import math
from algorithms import minimax, alpha_beta, expectimax, count_connect4

class Board:
    def __init__(self, cols=7, rows=6):
        self.cols = cols
        self.rows = rows
        self.board = None
        self.reset()
    
    def reset(self):
        # 0 = empty, 1 = human (red), 2 = AI (yellow)
        self.board = np.zeros((self.rows, self.cols), dtype=int)
    
    def drop_piece(self, column, player):
        if not self.is_valid_column(column):
            return False
        
        # Find the lowest empty row in the column
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][column] == 0:
                self.board[row][column] = player
                return True
        return False
    
    def is_valid_column(self, column):
        if column < 0 or column >= self.cols or column is None:
            return False
        return self.board[0][column] == 0
    
    def get_valid_columns(self):
        return [col for col in range(self.cols) if self.is_valid_column(col)]
    
    def is_full(self):
        return all(self.board[0][col] != 0 for col in range(self.cols))
    
    def count_connected_fours(self, player):
        # Convert board to list format for algorithms.count_connect4
        board_list = self.board.tolist()
        return count_connect4(board_list, player)
    
    def get_scores(self):
        human_score = self.count_connected_fours(1)
        ai_score = self.count_connected_fours(2)
        return human_score, ai_score
    
    def get_winner(self):
        if not self.is_full():
            return None
        
        human_score, ai_score = self.get_scores()
        if human_score > ai_score:
            return 1  # Human wins
        elif ai_score > human_score:
            return 2  # AI wins
        else:
            return 0  # Draw

class Game:
    def __init__(self, cols=7, rows=6):
        self.board = Board(cols, rows)
        self.current_player = 1  # 1 = Human, 2 = AI
        self.game_over = False
        self.winner = None
        self.draw = False
        self.ai_algorithm = "minimax"
        self.search_depth = 4  # K value
        
    def switch_player(self):
        self.current_player = 2 if self.current_player == 1 else 1
    
    def make_move(self, column):
        if self.game_over or not self.board.is_valid_column(column):
            return False
        
        # Drop the piece
        success = self.board.drop_piece(column, self.current_player)
        
        if success:
            # Check if board is full
            if self.board.is_full():
                self.game_over = True
                winner = self.board.get_winner()
                if winner == 1:
                    self.winner = 1
                elif winner == 2:
                    self.winner = 2
                else:
                    self.draw = True
            
            # Switch player if game not over
            if not self.game_over:
                self.switch_player()
        
        return success
    
    # AI INTEGRATION
    def get_ai_move(self):
        board_list = self.board.board.tolist()
        
        if self.ai_algorithm == "minimax":
            col, _ = minimax(board_list, self.search_depth, True)
            
        elif self.ai_algorithm == "alphabeta":
            col, _ = alpha_beta(board_list, self.search_depth, -math.inf, math.inf, True)
            
        elif self.ai_algorithm == "expectimax":
            col, _ = expectimax(board_list, self.search_depth, True)
            
        else:
            col = None
            
        return col
    
    def play_ai_turn(self):
        if self.current_player != 2 or self.game_over:
            return
        
        col = self.get_ai_move()
        
        if col is not None:
            self.make_move(col)
            
    def reset_game(self):
        self.board.reset()
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.draw = False