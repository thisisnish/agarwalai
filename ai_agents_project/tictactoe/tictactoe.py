"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

ROWS = 3
COLS = 3

PLAYER_X = True


def is_player_x():
    global PLAYER_X
    return PLAYER_X

def change_player(board):
    global PLAYER_X
    PLAYER_X = not PLAYER_X

def is_horizontal_win(board):
        for i in range(ROWS):
            for player in [X, O]:
                count = 0
                for j in range(COLS):
                    if board[i][j] == player:
                        count += 1
                    if count == 3:
                        return player
        return None
    
def is_vertical_win(board):
        for i in range(ROWS):
            for player in [X, O]:
                count = 0
                for j in range(COLS):
                    if board[j][i] == player:
                        count += 1
                    if count == 3:
                        return player
        return None
    
def is_diagonaol_win(board):
        for player in [X, O]:
            count = 0
            for i in range(ROWS):
                if board[i][i] == player:
                    count += 1
                if count == 3:
                    return player

            count = 0
            for i in range(ROWS):
                if board[i][COLS-1-i] == player:
                    count += 1
                if count == 3:
                    return player

        return None
    
def is_full(board):
        full = True
        for i in range(ROWS):
            for j in range(COLS):
                if board[i][j] is EMPTY:
                    full = False
        return full

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    return X if PLAYER_X else O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j]:
                continue
            actions.append((i, j))

    return actions

def result(board, action, player=None):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    global PLAYER_X

    i, j = action
    if board[i][j]:
        raise ValueError

    result_board = copy.deepcopy(board)
    result_board[i][j] = player if player else X if PLAYER_X else O
    return result_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner_p = is_diagonaol_win(board)
    if winner_p:
        return winner_p
    
    winner_p = is_horizontal_win(board)
    if winner_p:
        return winner_p
    
    return is_vertical_win(board)


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    
    return is_full(board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_p = winner(board)
    if winner_p == X:
        return 1
    elif winner_p == O:
        return -1
    else:
        return 0


def minValue(board):
    global PLAYER_X
    if terminal(board):
        return utility(board)
    v = float("inf")
    actionss = actions(board)

    for action in actionss:
        v = min(v, utility(result(board, action, O if PLAYER_X else X)))

    return v

def maxValue(board):
    global PLAYER_X
    if terminal(board):
        return utility(board)
    v = float("-inf")
    actionss = actions(board)

    for action in actionss:
        v = max(v, utility(result(board, action, O if PLAYER_X else X)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    actionss = actions(board)

    v = float("-inf") if is_player_x() else float('inf')

    move = actionss[0]
    for action in actionss:
        new_v = max(v, minValue(result(board, action))) if is_player_x() else min(v, maxValue(result(board, action)))
        if (new_v > v and is_player_x()) or (new_v < v and not is_player_x()):
            move = action
            v = new_v

    return move
