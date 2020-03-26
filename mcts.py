# https://medium.com/@arnavparuthi/playing-ultimate-tic-tac-toe-using-reinforcement-learning-892f084f7def
import numpy as np

class MCTS:
    def __init__(self, board):
        self.tree = {(board.current_state(), 0, 0) : np.array([])}
        self.path = [(board.current_state(), 0, 0)]
        self.c = np.sqrt(2)

    def traverse(self):
        s0 = self.path[-1]
        if s0 not in self.tree:
            self.tree[s0] = np.array([])



    def expand(self):
        self.tree[self.path[-1]] = [()]