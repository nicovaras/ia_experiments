from PIL import Image, ImageDraw, ImageFont,ImageEnhance
from itertools import chain

FILE = 'test.jpg'
COLORS = 4
TURNS = 4

class Kami(object):
    def __init__(self, image):
        self.image = image

    def solve(self):
        self._preprocess()
        colors = self._colors()
        board = self._build_board()
        board_colors = self._assing_colors_to_board(colors, board)
        # return self._solution_from(colors, board, board_colors)


    def _assing_colors_to_board(self, colors, board):
        board_colors = {}
        for x,y in board:
            pixel_color = self._average_color(x, y)
            board_colors[(x,y)] = self._closest_color(colors, pixel_color)
        return board_colors

    def _average_color(self, x, y):
        avg_color = (0,0,0)
        count = 0
        for i in range(-15,15):
            for j in range(-15,15):
                if x+i >0 and y+j > 0:
                    count += 1
                    color = self.image.getpixel((x+i, y+j))
                    avg_color = color[0]+avg_color[0],color[1]+avg_color[1],color[2]+avg_color[2]
        avg_color =  avg_color[0]/count,avg_color[1]/count,avg_color[2]/count
        return avg_color

    def _board_positions(self):
        odd_lines = self._points_from_row(10, 0, 82, 110)
        even_lines = self._points_from_row(40, 30, 84, 50)

        return list(chain(*zip(odd_lines, even_lines)))[:-1]

    def _build_board(self):
        positions = self._board_positions()
        board = self._build_board_from(positions)
        return board

    def _build_board_from(self, positions):
        board = {}
        for line_index in range(len(positions)):
            for pos_index in range(len(positions[line_index])):
                x,y = positions[line_index][pos_index]
                board[(x,y)] = self._neighbours_for(positions, line_index, pos_index)
        return board

    def _closest_color(self, colors, pixel_color):
        min_distance = 99999
        closest = None
        for c in colors:
            distance = sum([abs(c1-c2) for c1,c2 in zip(c, pixel_color)])
            if distance < min_distance:
                min_distance = distance
                closest = c
        return closest

    def _colors(self):
        colors = []
        starting_x, starting_y = 340, 1220
        separation = 100
        for i in range(COLORS):
            colors.append(self._average_color(starting_x + i*separation, starting_y))
        return colors

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
        for j in range(0, 1200, step):
            line = []
            for i in range(0, 680, 145):
                line.append((x + i, y + j))
                line.append((x + i + separation, y + j))
            lines.append(line)
        return lines

    def _preprocess(self):
        enhancer = ImageEnhance.Color(self.image)
        self.image = enhancer.enhance(2.0)

    def _solution_from(self, colors, board, board_colors):
        solution = []
        if tries > TURNS:
            return
        for (x,y) in board:
            paint(x,y)
            if solved():
                return solution
            recur_from(x.y)
            unpaint(x,y)




def get_image():
    return Image.open(FILE).convert('RGB')

image = get_image()
kami = Kami(image)
kami._preprocess()
colors = kami._colors()
board = kami._build_board()
board_colors = kami._assing_colors_to_board(colors, board)

d = ImageDraw.Draw(image)
font = ImageFont.truetype("font.ttf", 20)
for x1 in board:
    for x2 in board[x1]:
        d.line((x1,x2), fill='#666666')
        d.text((x2[0]-10,x2[1]-10), str(colors.index(board_colors[x2])),fill='#000000',font=font)
image.show()



