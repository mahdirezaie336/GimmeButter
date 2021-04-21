import pygame
from constants import Consts
import threading


class Display:

    display_thread: threading.Thread

    def __init__(self, map_array, w, h, points):
        self.map_array = map_array
        self.w = w
        self.h = h
        self.points = points

        # PyGame part
        pygame.init()
        sw, sh = Consts.SCREEN_WIDTH, Consts.SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((sw, sh))
        self.screen.fill(Consts.BACKGROUND)

        # Setting cell size and other sizes
        self.draw_cells()

        pygame.display.update()
        # Threading part
        self.display_thread = None

    def update(self):
        pass

    def draw_cells(self):
        sw, sh = Consts.SCREEN_WIDTH, Consts.SCREEN_HEIGHT
        w, h = self.w, self.h

        if w / h > sw / sh:
            rect_width = sw - 2 * Consts.SCREEN_MARGIN_SIZE
            cell_size = int(rect_width / w)
            rect_height = cell_size * h
        else:
            rect_height = sh - 2 * Consts.SCREEN_MARGIN_SIZE
            cell_size = int(rect_height / h)
            rect_width = cell_size * w

        # Drawing cells
        init_y = (sh - rect_height) / 2
        init_x = (sw - rect_width) / 2
        for j in range(h):
            for i in range(w):
                x = init_x + i * cell_size
                y = init_y + j * cell_size
                if self.map_array[j][i] == 'x':
                    color = Consts.BLOCK_COLOR
                else:
                    color = Display.darker(Consts.CELL_COLOR, int(self.map_array[j][i]))
                # Drawing Rectangles
                pygame.draw.rect(self.screen, color, (x, y, cell_size, cell_size), 0)
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, cell_size, cell_size), 1)

    def begin_display(self):

        def infinite_loop():
            """ This is the function which includes the infinite loop for pygame pumping. """
            while True:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        exit()

                pygame.display.update()
                pygame.time.wait(100)

        # Starting thread
        self.display_thread = threading.Thread(name='Display', target=infinite_loop)
        self.display_thread.start()

    @staticmethod
    def darker(color: tuple[int, int, int], radius: int):
        r = color[0] - (radius - 1) * 30
        g = color[1] - (radius - 1) * 30
        b = color[2] - (radius - 1) * 30
        r = 0 if r < 0 else r
        g = 0 if g < 0 else g
        b = 0 if b < 0 else b
        return r, g, b
