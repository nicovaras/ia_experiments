class HitoriSolver(object):

    def __init__(self, board):
        self.board = board
        self.available = len(board)**2

    def repeated_in_col(self, i, j):
        return any([self.board[i][j] == self.board[row][j] for row in range(len(self.board)) if row != i])

    def repeated_in_row(self, i, j):
        return any([self.board[i][j] == self.board[i][col] for col in range(len(self.board)) if col != j])

    def first_number_position(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] != '*':
                    return (i, j)

    def still_connected(self):
        stack = [self.first_number_position()]
        visited = set()
        connected = 0
        while stack:
            curr = stack.pop()
            visited.add(curr)
            connected += 1

            for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if 0 <= curr[0] + x < len(self.board) and 0 <= curr[1] + y < len(self.board):
                    if self.board[curr[0] + x][curr[1] + y] != '*' and (curr[0] + x, curr[1] + y) not in visited:
                        stack.append((curr[0] + x, curr[1] + y))
                        visited.add((curr[0] + x, curr[1] + y))

        return connected == self.available

    def is_solved(self):
        solved = self.still_connected()
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                solved &= self.board[i][j] == "*" or (not self.repeated_in_col(i, j) and
                                                      not self.repeated_in_row(i, j))
        return solved

    def is_nullable(self, i, j):
        neighbour_not_nulled = all([
            self.board[i + x][j + y] != '*' for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if 0 <= i + x < len(self.board) and 0 <= j + y < len(self.board)
        ])
        return self.board[i][j] != '*' and neighbour_not_nulled and (self.repeated_in_row(i, j) or
                                                                     self.repeated_in_col(i, j))

    def set_at(self, i, j, char):
        if char == '*':
            self.available -= 1
        elif self.board[i][j] == '*':
            self.available += 1
        self.board[i][j] = char

    def solve_from(self, i, j):
        while i < len(self.board):
            while j < len(self.board):
                if self.is_nullable(i, j):
                    tmp = self.board[i][j]
                    self.set_at(i, j, '*')
                    self.solve_from(i, j)
                    if self.is_solved():
                        return self.board
                    self.set_at(i, j, tmp)
                j += 1
            j = 0
            i += 1
        return None

    def solve(self):
        return self.solve_from(0, 0)
