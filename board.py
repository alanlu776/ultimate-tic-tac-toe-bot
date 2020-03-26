import numpy as np


def game():
    b = Board(True)
    m = (0, 0)
    print(b)
    while not check_win(b.boards_won, *m):
        while True:
            m = input("> ").split(', ')
            if len(m) != 2: # right number of coordinates
                continue

            try:
                m = tuple(map(int, m))
            except:
                continue

            if b.is_valid_move(m[0], m[1]):
                break
            print(f"Move must be between ({b.sub_board[1]}, {b.sub_board[0]}) "
                  f"and ({b.sub_board[3]}, {b.sub_board[2]})")

        b = b.make_move(m[1] * 9 + m[0])
        m = (m[0] // 3, m[1] // 3)
        print(b)
        print(b.boards_won)


def check_win(board, x, y):
    winner = board[y][x]

    for j in range(len(board[0])):
        if board[y][j] != winner:
            break
    else:
        return winner

    for i in range(len(board)):
        if board[i][x] != winner:
            break
    else:
        return winner

    # check diagonals
    if x == y:
        for i in range(len(board)):
            if board[i][i] != winner:
                break
        else:
            return winner

    if x + y == len(board) - 1:
        for i in range(len(board)):
            if board[i][len(board) - 1 - i] != winner:
                break
        else:
            return winner

    # check for draw
    for i in board:
        for j in i:
            if not j:
                # no winner yet
                return None

    # draw
    return 0


class Board:
    def __init__(self, state=None, show_lines=False):
        self.show_lines = show_lines
        if state is None:
            self.state = np.array([[0] * 9 for _ in range(9)])
            self.boards_won = np.array([[None] * 3 for _ in range(3)])
            self.move = -1 # player 1
            # represents the coordinates of the current sub board the player is able to play
            # self.sub_board = np.array([0, 0, 9, 9])
            self.min = np.array([0, 0])
            self.max = np.array([9, 9])
        # else:
        #     self.state =

    def board_state(self):
        return self.state.flatten(), np.concatenate((self.min, self.max)), self.boards_won, self.move

    def current_state(self):
        return self.state.flatten(), np.concatenate((self.min, self.max))

    def possible_moves(self):
        moves = []
        # find all non-empty spots on the sub board
        for i in range(self.min[0], self.max[0]):
            for j in range(self.min[1], self.max[1]):
                if self.is_valid_move(j, i):
                    moves.append(i * 9 + j)
        return moves

    def valid_moves(self):
        # similar function that outputs a 1D array for the neural network
        return np.ones(self.state.shape) - np.absolute(self.state)

    def is_valid_move(self, x, y):
        return self.min[0] <= y < self.max[0] and \
               self.min[1] <= x < self.max[1] and \
               self.boards_won[y // 3][x // 3] is None and \
               not self.state[y][x]

    def make_move(self, index):
        y = index // 9
        x = index % 9

        # copy current board
        new_board = Board(self.show_lines)
        new_board.state = np.copy(self.state)
        new_board.state[y][x] = self.move
        new_board.move = -self.move

        # coordinates of the sub board the move was on and the next sub board
        coords = np.array([y, x])
        m_min = np.floor_divide(coords, 3) * 3
        m_max = m_min + 3
        new_board.min = (coords - m_min) * 3
        new_board.max = new_board.min + 3

        # check if the sub board is now won from the position of x and y (converted to between the sub_board)
        is_won = check_win(new_board.state[m_min[0]:m_max[0], m_min[1]:m_max[1]],
                           x - m_min[1], y - m_min[0])

        # copy over any boards that can't be visited anymore
        new_board.boards_won = np.copy(self.boards_won)
        if is_won is not None:
            new_board.boards_won[y // 3][x // 3] = is_won

        # check if the move is in a sub board that has been won
        if new_board.boards_won[y - m_min[0]][x - m_min[1]] is not None:
            new_board.min = np.array([0, 0])
            new_board.max = np.array([len(self.state), len(self.state[0])])
        return new_board

    def __repr__(self):
        # return " \n".join([repr(["X" if e == -1 else "O" if e == 1 else " " for e in s]) for s in self.state])
        result = ""
        for i in range(len(self.state)):
            if self.show_lines and (i == 3 or i == 6):
                result += '-' * 11 + '\n'
            for j in range(len(self.state[0])):
                if self.show_lines and (j == 3 or j == 6):
                    result += '|'
                if self.boards_won[i // 3][j // 3] is not None:
                    result += '_' if not self.boards_won[i // 3][j // 3] else 'X' if self.boards_won[i // 3][j // 3] == -1 else 'O'
                else:
                    result += ' ' if not self.state[i][j] else 'X' if self.state[i][j] == -1 else 'O'
            result += '\n'
        return result