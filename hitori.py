from utils import get_window_position
from mss import mss
import numpy as np
import cv2
import pytesser
import autopy
import pprint


class HitoriSolver(object):

    def __init__(self, board):
        self.board = board
        self.available = len(board)**2

    def repeated_in_col(self, i, j):
        return any([self.board[i][j] == self.board[row][j] for row in range(len(self.board)) if row != i])

    def repeated_in_row(self, i, j):
        return any([self.board[i][j] == self.board[i][col] for col in range(len(self.board)) if col != j])

    def still_connected(self, i, j):
        for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if 0 <= i + x < len(self.board) and 0 <= j + y < len(self.board):
                root = (i + x, j + y)
        stack = [root]
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
        # if connected == self.available:
        # print self.available
        return connected == self.available

    def is_solved(self):
        solved = True
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

    def solve(self):
        if self.is_solved():
            return self.board
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.is_nullable(i, j):
                    tmp = self.board[i][j]
                    self.board[i][j] = '*'
                    self.available -= 1
                    if self.still_connected(i, j) and self.solve() is not None:
                        return self.board
                    self.board[i][j] = tmp
                    self.available += 1
        return None


if __name__ == "__main__":
    sct = mss()
    mon = get_window_position("Hitori")
    pixels = sct.get_pixels(mon)
    im = np.fromstring(pixels, np.uint8).reshape(mon['height'], mon['width'], 3)
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 60, 255, 1)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    x, y, w, h = cv2.boundingRect(contours[0])

    contours = [cnt for cnt in contours if cv2.contourArea(cnt) == cv2.contourArea(contours[1])]
    cv2.drawContours(thresh, contours, -1, (0, 0, 0), 3)

    thresh = thresh[y + 2:y + h - 2, x + 2:x + w - 2]
    nums = pytesser.iplimage_to_string(thresh, psm=11, config="tessedit_char_whitelist=0123456789").strip().split()
    nums = [list(x) for x in nums]
    pprint.pprint(nums)

    solution = HitoriSolver(nums).solve()
    pprint.pprint(solution)

    rects = [cv2.boundingRect(c) for c in contours][::-1]
    valid_rects = []
    for i in range(len(solution)):
        for j in range(len(solution)):
            if solution[i][j] == '*':
                valid_rects.append(rects[i * len(solution) + j])

    for x, y, h, w in valid_rects:
        autopy.mouse.smooth_move(x + w / 2 + mon['left'], y + h / 2 + mon['top'])
        autopy.mouse.click()
