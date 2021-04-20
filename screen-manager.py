import pygame
from constants import Consts
import threading


class Display:

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
        if w / h > sw / sh:
            rect_width = sw - 2 * Consts.SCREEN_MARGIN_SIZE
            cell_size = int(rect_width / w)
            rect_height = cell_size * h
        else:
            rect_height = sh - 2 * Consts.SCREEN_MARGIN_SIZE
            cell_size = int(rect_height / h)
            rect_width = cell_size * w
        pygame.draw.rect(self.screen, )
        # Threading part
        self.display_thread = None

    def update(self):
        pass

    def begin_display(self):
        def infinite_loop():
            while True:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        exit()

                pygame.display.update()
                pygame.time.wait(100)

        self.display_thread = threading.Thread(name='Display', target=infinite_loop)
        self.display_thread.start()
