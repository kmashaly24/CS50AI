"""
Tic Tac Toe Player
"""

import math
import copy
import numpy as np

X = "X"
O = "O"
EMPTY = None


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
    if board == initial_state():
        return X
    elif board.count(X) > board.count(O):
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    new_board = copy.deepcopy(board)
    if board[i][j] == EMPTY and action in actions(board):
        new_board[i][j] = player(board)
        return new_board
    else:
        raise Exception("Invalid action")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    new_board = copy.deepcopy(board)

    for i in range(3):
        for j in range(3):
            if new_board[i][j] == X:
                new_board[i][j] = 1
            elif new_board[i][j] == O:
                new_board[i][j] = -1
            else:
                new_board[i][j] = 0

    new_board = np.array(new_board)

    sumss = []
    for i in range(3):
        sumss.append(new_board.sum(axis=1)[i])     
        sumss.append(new_board.sum(axis=0)[i]) 
        
    sumss.append(new_board.diagonal().sum())
    sumss.append(np.fliplr(new_board).diagonal().sum())

    if 3 in sumss:
        return X
    elif -3 in sumss:
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if any([winner(board) is not None ,len(actions(board)) == 0]):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        win = winner(board)
        if win == X:
            return 1
        elif win == O:
            return -1
        else:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def max_value(board):

        max_action = None
        v = -math.inf

        if terminal(board):
            return utility(board), None   
        
        else:
            for action in  actions(board):
                min_val, _ = min_value(result(board, action))
                if min_val > v:
                    v = min_val
                    max_action = action
                if v == 1:
                    break
            return v, max_action
        
    def min_value(board):
        min_action = {}
        v = math.inf

        if terminal(board):
            return utility(board), None
        else:
            v = math.inf
            for action in actions(board):
                max_val, _ = max_value(result(board, action))
                if max_val < v:
                    v = max_val
                    min_action = action
                if v == -1:
                    break
            return v, min_action

    if player(board) == X:
        _, best_move = max_value(board)
    else:
        _, best_move = min_value(board)
    
    return best_move
    
