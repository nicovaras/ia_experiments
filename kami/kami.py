from PIL import Image, ImageDraw
from itertools import chain

FILE = 'test.jpg'
COLORS = 4

class Kami(object):
    def __init__(self, image):
        self.image = image

    def solve(self):
        colors = self.get_colors()
        board = self.build_board()
        return self.get_solution_from(colors, board)

    def get_solution_from(self, colors, board):
        pass

    def build_board(self):
        d = ImageDraw.Draw(self.image)
        positions = self._get_board_positions()
        board = self._build_board_from(positions)
        for x1 in board:
            for x2 in board[x1]:
                d.line((x1,x2))
                d.ellipse([x2[0]-3, x2[1]-3, x2[0]+3, x2[1]+3], fill="#fafafa")
        self.image.show()
        return board

    def get_colors(self):
        colors = []
        starting_x, starting_y = 340, 1220
        separation = 100
        for i in range(COLORS):
            colors.append(self.image.getpixel((starting_x + i*separation, starting_y)))
        return colors

    def _get_board_positions(self):
        odd_lines = self._points_from_row(10, 0, 82, 110)
        even_lines = self._points_from_row(40, 30, 84, 50)

        return list(chain(*zip(odd_lines, even_lines)))

    def _build_board_from(self, positions):
        board = {}
        for line_index in range(len(positions)):
            for pos_index in range(len(positions[line_index])):
                x,y = positions[line_index][pos_index]
                board[(x,y)] = self._neighbours_for(positions, line_index, pos_index)
        return board

    def _neighbours_for(self, positions, line, pos):
        neighbours = []
        if line > 0:
            neighbours.append(positions[line-1][pos])
        if line < len(positions)-1:
            neighbours.append(positions[line+1][pos])
        if line % 2 == 0:
            if pos % 2 == 0 and pos > 0:
                neighbours.append(positions[line][pos-1])
        else:
            if pos % 2 == 0 and pos < len(positions[line]) - 1:
                neighbours.append(positions[line][pos+1])
        return neighbours

    def _points_from_row(self, starting_x, starting_y, step, separation):
        x, y = starting_x, starting_y
        lines = []
        for j in range(0, 1270, step):
            line = []
            for i in range(0, 780, 145):
                line.append((x + i, y + j))
                line.append((x + i + separation, y + j))
            lines.append(line)
        return lines

def get_image():
    return Image.open(FILE).convert('RGB')

image = get_image()
kami = Kami(image)
kami.build_board()




