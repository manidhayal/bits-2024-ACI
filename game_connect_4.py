import math
import random

# Constants for grid size and players
ROWS = 6
COLS = 7
PLAYER = 1  # Human player
AI = 2  # Computer player
EMPTY = 0
DEPTH = 3

# Create empty 7x6 grid
def create_grid():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

# Display grid function
def print_grid(grid):
    for row in grid:
        print(row)
    print()

# Check if a column has space for another disc
def is_valid_column(grid, col):
    return grid[0][col] == EMPTY

# Find the next available row in a column
def get_next_open_row(grid, col):
    for row in range(ROWS - 1, -1, -1):
        if grid[row][col] == EMPTY:
            return row

# Drop a disc in the grid
def drop_piece(grid, row, col, piece):
    grid[row][col] = piece

# Check if there's a win
def winning_move(grid, piece):
    # Check horizontal locations
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(grid[r][c+i] == piece for i in range(4)):
                return True
    
    # Check vertical locations
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(grid[r+i][c] == piece for i in range(4)):
                return True
    
    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(grid[r+i][c+i] == piece for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(grid[r-i][c+i] == piece for i in range(4)):
                return True
    return False

# Check if the grid is full (draw condition)
def is_draw(grid):
    return all(grid[0][c] != EMPTY for c in range(COLS))

# Evaluate the score of a window of 4 cells
def evaluate_window(window, piece):
    score = 0
    opponent = PLAYER if piece == AI else AI

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opponent) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

# Score the grid based on the current board state
def score_position(grid, piece):
    score = 0

    # Score center column for control
    center_array = [grid[r][COLS // 2] for r in range(ROWS)]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score horizontal positions
    for r in range(ROWS):
        row_array = [grid[r][c] for c in range(COLS)]
        for c in range(COLS - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    # Score vertical positions
    for c in range(COLS):
        col_array = [grid[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece)

    # Score positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [grid[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score negatively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [grid[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

# Minimax algorithm with pruning
def minimax(grid, depth, alpha, beta, maximizing_player):
    valid_columns = [c for c in range(COLS) if is_valid_column(grid, c)]
    is_terminal = winning_move(grid, PLAYER) or winning_move(grid, AI) or is_draw(grid)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(grid, AI):
                return (None, 100000000000000)
            elif winning_move(grid, PLAYER):
                return (None, -10000000000000)
            else: # Game is over, no valid moves (draw)
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(grid, AI))

    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_columns)
        for col in valid_columns:
            row = get_next_open_row(grid, col)
            temp_grid = [row[:] for row in grid]
            drop_piece(temp_grid, row, col, AI)
            new_score = minimax(temp_grid, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player (human)
        value = math.inf
        column = random.choice(valid_columns)
        for col in valid_columns:
            row = get_next_open_row(grid, col)
            temp_grid = [row[:] for row in grid]
            drop_piece(temp_grid, row, col, PLAYER)
            new_score = minimax(temp_grid, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

# Play Connect Four Game
def play_game():
    grid = create_grid()
    print_grid(grid)
    game_over = False
    turn = random.choice([PLAYER, AI])

    while not game_over:
        if turn == PLAYER:
            # Human player input with error checking
            while True:
                try:
                    col = int(input("Human player, choose a column (0-6): "))
                    if col < 0 or col >= COLS:
                        print("Invalid column. Please choose a column between 0 and 6.")
                    elif not is_valid_column(grid, col):
                        print("Column is full. Choose another one.")
                    else:
                        break
                except ValueError:
                    print("Invalid input. Please enter a number between 0 and 6.")

            row = get_next_open_row(grid, col)
            drop_piece(grid, row, col, PLAYER)

            if winning_move(grid, PLAYER):
                print_grid(grid)
                print("Human wins!")
                game_over = True

            if is_draw(grid):
                print_grid(grid)
                print("It's a draw!")
                game_over = True

            turn = AI

        else:
            col, minimax_score = minimax(grid, DEPTH, -math.inf, math.inf, True)
            row = get_next_open_row(grid, col)
            drop_piece(grid, row, col, AI)

            if winning_move(grid, AI):
                print_grid(grid)
                print("Computer wins!")
                game_over = True

            if is_draw(grid):
                print_grid(grid)
                print("It's a draw!")
                game_over = True

            turn = PLAYER

        print_grid(grid)

# Start the game
play_game()
