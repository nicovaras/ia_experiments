from common.utils import get_image_from_window, get_window_position, click_regions, click_at
from processor import HitoriProcessor
from solver import HitoriSolver
import pprint


class HitoriPlayer(object):

    def __init__(self):
        self.window_position = None
        self.nums = None
        self.processor = None
        self.solution = None

    def detect_numbers(self):
        image = get_image_from_window(self.window_position)
        self.processor = HitoriProcessor(image)
        self.nums = self.processor.detect_numbers()
        print 'OpenCV detection'
        pprint.pprint(self.nums)

    def solve(self):
        self.solution = HitoriSolver(self.nums).solve()
        print '\nSolution'
        pprint.pprint(self.solution)

    def click_solution(self):
        valid_rects = []
        for i in range(len(self.solution)):
            for j in range(len(self.solution)):
                if self.solution[i][j] == '*':
                    valid_rects.append(self.processor.bounding_rects[i * len(self.solution) + j])
        click_regions(self.window_position['left'], self.window_position['top'], valid_rects)

    def click_play_again(self):
        click_at(self.window_position['left'], self.window_position['top'], (275, 275))

    def play(self):
        self.window_position = get_window_position("Hitori")
        self.detect_numbers()
        self.solve()
        self.click_solution()

    def play_again(self):
        self.click_play_again()
