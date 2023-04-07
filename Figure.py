import random

import pygame as pg
import Field

fig_s = 5
block = 20
colors = {'S': (100, 255, 0),
          'Z': (255, 0, 0),
          'J': (0, 0, 255),
          'L': (255, 150, 0),
          'I': (0, 200, 255),
          'O': (255, 250, 0),
          'T': (220, 0, 255)}

figures = {'S': [['ooooo',
                  'ooooo',
                  'ooxxo',
                  'oxxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxxo',
                  'oooxo',
                  'ooooo']],
           'Z': [['ooooo',
                  'ooooo',
                  'oxxoo',
                  'ooxxo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'oxxoo',
                  'oxooo',
                  'ooooo']],
           'J': [['ooooo',
                  'oxooo',
                  'oxxxo',
                  'ooooo',
                  'ooooo'],
                 ['ooooo',
                  'ooxxo',
                  'ooxoo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'oxxxo',
                  'oooxo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxoo',
                  'oxxoo',
                  'ooooo']],
           'L': [['ooooo',
                  'oooxo',
                  'oxxxo',
                  'ooooo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxoo',
                  'ooxxo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'oxxxo',
                  'oxooo',
                  'ooooo'],
                 ['ooooo',
                  'oxxoo',
                  'ooxoo',
                  'ooxoo',
                  'ooooo']],
           'I': [['ooxoo',
                  'ooxoo',
                  'ooxoo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'xxxxo',
                  'ooooo',
                  'ooooo']],
           'O': [['ooooo',
                  'ooooo',
                  'oxxoo',
                  'oxxoo',
                  'ooooo']],
           'T': [['ooooo',
                  'ooxoo',
                  'oxxxo',
                  'ooooo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxxo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'oxxxo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'oxxoo',
                  'ooxoo',
                  'ooooo']]}


class Figure:
    def __init__(self, surface):
        self.surface = surface
        self.shape = random.choice(list(figures.keys()))
        self.rotation = random.randint(0, len(figures[self.shape]) - 1)
        self.color = colors.get(self.shape)
        self.x = int(Field.field_w / 2) - int(fig_s / 2)
        self.y = -2

    def draw_block(self, block_x, block_y, color, pixelx=None, pixely=None):
        if color == Field.empty:
            return
        if pixelx == None and pixely == None:
            pixelx, pixely = self.convert_coords(block_x, block_y)
        pg.draw.rect(self.surface, color, (pixelx + 1, pixely + 1, block - 1, block - 1), 0, 3)

    def draw_fig(self, pixelx=None, pixely=None):
        figToDraw = figures[self.shape][self.rotation]
        if pixelx == None and pixely == None:
            pixelx, pixely = self.convert_coords(self.x, self.y)

        for x in range(fig_s):
            for y in range(fig_s):
                if figToDraw[y][x] != Field.empty:
                    self.draw_block(None, None, self.color, pixelx + (x * block), pixely + (y * block))

    def convert_coords(self, block_x, block_y):
        return (Field.side_margin + (block_x * block)), (Field.top_margin + (block_y * block))
