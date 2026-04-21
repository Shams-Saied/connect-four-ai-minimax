import math
import copy
import time
ROWS = 6
COLS = 7

def get_valid_moves(board):
    valid = [c for c in range(COLS) if board[0][c] == 0]
    center = COLS // 2
    return sorted(valid, key=lambda x: abs(x - center)) # priortized center to increase early pruning

def drop_piece(board, col, piece):
    new_board = copy.deepcopy(board) # copy the board and nested lists
    for r in reversed(range(ROWS)): # loop through rows from bottom to up
        if new_board[r][col] == 0: # drop piece once empty spot found
            new_board[r][col] = piece
            break
    return new_board

# board is full
def is_terminal(board):
    return len(get_valid_moves(board)) == 0

# count how many 4 in a row the player has
def count_connect4(board, piece):
    count = 0
    
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                count += 1
    
    # Vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                count += 1
    
    # Diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                count += 1
    
    # Diagonal /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                count += 1
                
    return count


# HEURISTIC 
def evaluate_window(window, piece): # evaluate a window of 4 cells
    score = 0
    opponent = 1 if piece == 2 else 2 # to know opponent's piece
    
    if window.count(piece) == 4: # 4 in a row
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1: # 3 pieces and an empty spot
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2: # 2 with 2 empty spots
        score += 2
    
    if window.count(opponent) == 3 and window.count(0) == 1: # to block opponent from winning
        score -= 4
        
    return score


def evaluate(board):
    score = 0
    
    # connect-4 scoring 
    score += count_connect4(board, 2) * 100
    score -= count_connect4(board, 1) * 100
    
    # Center preference
    center = [board[r][COLS//2] for r in range(ROWS)] # list of all values in center column
    score += center.count(2) * 3
    
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            window = [board[r][c+i] for i in range(4)] # extract 4 cells horizontally
            score += evaluate_window(window, 2) # add window score to total
            
    # Vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            window = [board[r+i][c] for i in range(4)]
            score += evaluate_window(window, 2)
            
    # Diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, 2)
            
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, 2)
            
    return score

# MINIMAX (NO PRUNING)

minimax_node_count = 0

def minimax(board, depth, maximizingPlayer, indent=""):
    
    global minimax_node_count
    minimax_node_count += 1
    valid_moves = get_valid_moves(board)
    
    # Base case: depth limit reached or terminal state
    if depth == 0 or not valid_moves:
        if not valid_moves:  # Terminal state (board full)
            ai_score = count_connect4(board, 2)
            human_score = count_connect4(board, 1)
            return None, (ai_score - human_score) * 1000
        else:  # Depth limit reached
            h = evaluate(board)
            print(indent + f"HEURISTIC VALUE = {h}")
            return None, h
        
    # MAX PLAYER (AI)
    if maximizingPlayer:
        value = -math.inf
        best_col = valid_moves[0]
        
        for col in valid_moves:
            child = drop_piece(board, col, 2)  # AI piece = 2
            _, new_score = minimax(child, depth - 1, False, indent + "   ")
            
            print(indent + f"MAX col={col}, score={new_score}")
            
            if new_score > value:
                value = new_score
                best_col = col
        
        return best_col, value
    
    # MIN PLAYER (HUMAN)
    else:
        value = math.inf
        best_col = valid_moves[0]
        
        for col in valid_moves:
            child = drop_piece(board, col, 1)  # Human piece = 1
            _, new_score = minimax(child, depth - 1, True, indent + "   ")
            
            print(indent + f"MIN col={col}, score={new_score}")
            
            if new_score < value:
                value = new_score
                best_col = col
        
        return best_col, value

#ALPHA-BETA

node_count = 0 # for performance comparison

def alpha_beta(board, depth, alpha, beta, maximizingPlayer, indent=""):
    global node_count # use global var
    node_count += 1 # node is being expanded
    valid_moves = get_valid_moves(board)
    
    # TERMINAL OR DEPTH LIMIT (K) (Base case)
    if depth == 0 or is_terminal(board):
        if is_terminal(board):
            ai_score = count_connect4(board, 2)
            human_score = count_connect4(board, 1)
            return None, (ai_score - human_score) * 1000 # none bec we arent choosing a col
        else:
            h = evaluate(board)
            print(indent + f"HEURISTIC VALUE = {h}")
            return None, h

    # MAX PLAYER (AI)
    if maximizingPlayer:
        value = -math.inf
        best_col = valid_moves[0] # default
        
        for col in valid_moves:
            child = drop_piece(board, col, 2)
            _, new_score = alpha_beta(child, depth-1, alpha, beta, False, indent+"   ")
            
            print(indent + f"MAX col={col}, score={new_score}")
            
            if new_score > value:
                value = new_score
                best_col = col
                
            alpha = max(alpha, value)
            # PRUNING
            if alpha >= beta:
                print(indent + "PRUNE MAX")
                break
            
        return best_col, value
    
    # MIN PLAYER (HUMAN)
    else:
        value = math.inf
        best_col = valid_moves[0]
        
        for col in valid_moves:
            child = drop_piece(board, col, 1)
            _, new_score = alpha_beta(child, depth-1, alpha, beta, True, indent+"   ")
            
            print(indent + f"MIN col={col}, score={new_score}")
            
            if new_score < value:
                value = new_score
                best_col = col
                
            beta = min(beta, value)
            
            if alpha >= beta:
                print(indent + "PRUNE MIN")
                break
            
        return best_col, value

# EXPECTED MINIMAX
expectimax_node_count = 0

def get_expected_probabilities(col):
    probs = {}
    probs[col] = probs.get(col, 0) + 0.6
    
    left = col - 1
    right = col + 1
    
    if 0 <= left < COLS:
        probs[left] = probs.get(left, 0) + 0.2
    else:
        probs[col] += 0.2
        
    if 0 <= right < COLS:
        probs[right] = probs.get(right, 0) + 0.2
    else:
        probs[col] += 0.2
        
    return probs

def expectimax(board, depth, maximizingPlayer, indent=""):
    global expectimax_node_count
    expectimax_node_count += 1
    
    valid_moves = get_valid_moves(board)
    
    if depth == 0 or not valid_moves:
        if not valid_moves:
            return None, (count_connect4(board, 2) - count_connect4(board, 1)) * 1000
        else:
            h = evaluate(board)
            print(indent + f"HEURISTIC VALUE = {h}")
            return None, h
        
    if maximizingPlayer:
        best_value = -math.inf
        best_col = valid_moves[0]
        
        for col in valid_moves:
            probs = get_expected_probabilities(col)
            
            exp_value = 0
            print(indent + f"EXPAND col={col} probs={probs}")
            
            for move_col, p in probs.items():
                _, v = expectimax(drop_piece(board, move_col, 2), depth-1, False, indent+"   ")
                exp_value += p * v
                
            print(indent + f"EXPECTED col={col} value={exp_value}")
            
            if exp_value > best_value:
                best_value = exp_value
                best_col = col
                
        return best_col, best_value
    
    else:
        best_value = math.inf
        best_col = valid_moves[0]
        
        for col in valid_moves:
            _, v = expectimax(drop_piece(board, col, 1), depth-1, True, indent+"   ")
            
            print(indent + f"MIN col={col}, score={v}")
            
            if v < best_value:
                best_value = v
                best_col = col
                
        return best_col, best_value


# UTILITY FUNCTIONS

# Heuristic fo each empty Cell
def print_board_heuristic(board):

    print("\n=== Board Heuristic Values ===")
    
    # Create a grid of heuristic contributions
    heuristic_grid = [[0]*COLS for _ in range(ROWS)]
    
    # For each empty cell, calculate what it would add to score
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == 0:  # Empty cell
                # Temporarily place AI piece
                temp_board = copy.deepcopy(board)
                temp_board[r][c] = 2
                # Calculate score difference
                heuristic_grid[r][c] = evaluate(temp_board) - evaluate(board)
    
    # Print grid
    print("\t0\t1\t2\t3\t4\t5\t6")
    for r in range(ROWS):
        print(f"{r}\t", end="")
        for c in range(COLS):
            if board[r][c] != 0:
                print(f"{board[r][c]}\t", end="")  # Show piece
            else:
                print(f"{heuristic_grid[r][c]}\t", end="")
        print()
    print("===============================\n")

# =============================
# TEST (K DEPTH)
def run_test(algorithm, K):
    
    board = [[0]*COLS for _ in range(ROWS)]  # empty board
    start_time = time.time()
    
    # Reset node counter and Run the selected algorithm
    if algorithm == "minimax":
        global minimax_node_count
        minimax_node_count = 0
        col, score = minimax(board, K, True)
        nodes_expanded = minimax_node_count
    elif algorithm == "alphabeta":
        global node_count
        node_count = 0
        col, score = alpha_beta(board, K, -math.inf, math.inf, True)
        nodes_expanded = node_count
    elif algorithm == "expectimax":
        global expectimax_node_count
        expectimax_node_count = 0
        col, score = expectimax(board, K, True)
        nodes_expanded = expectimax_node_count
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    return {
        "Algorithm": algorithm.capitalize(),
        "K": K,
        "Best Move": col,
        "Score": score,
        "Nodes": nodes_expanded,
        "Time": elapsed_time
    }

def demo_heuristic():
    print("\n=== Heuristic Demonstration ===")

    # Empty board
    board1 = [[0]*7 for _ in range(6)]
    print("Empty Board:")
    print_board_heuristic(board1)

    # Mid-game board
    board2 = [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,1,2,0,0,0],
        [0,2,1,2,0,0,0],
        [1,1,2,1,2,0,0]
    ]
    print("Mid Game Board:")
    print_board_heuristic(board2)
