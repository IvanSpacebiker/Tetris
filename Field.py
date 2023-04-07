import pygame as pg

import Figure

empty = 'o'
field_h, field_w = 20, 10
window_w, window_h = 600, 500

side_margin = int((window_w - field_w * Figure.block) / 2)
top_margin = window_h - (field_h * Figure.block) - 5


class Field:
    def __init__(self):
        self.field = []
        for i in range(field_w):
            self.field.append([empty] * field_h)

    def add_to_cup(self, fig):
        for x in range(Figure.fig_s):
            for y in range(Figure.fig_s):
                if Figure.figures[fig.shape][fig.rotation][y][x] != empty:
                    self.field[x + fig.x][y + fig.y] = fig.color

    def check_pos(self, fig, adjX=0, adjY=0):
        for x in range(Figure.fig_s):
            for y in range(Figure.fig_s):
                abovecup = y + fig.y + adjY < 0
                if abovecup or Figure.figures[fig.shape][fig.rotation][y][x] == empty:
                    continue
                if not (0 <= x + fig.x + adjX < field_w and y + fig.y + adjY < field_h):
                    return False
                if self.field[x + fig.x + adjX][y + fig.y + adjY] != empty:
                    return False
        return True

    def is_completed(self, y):
        for x in range(field_w):
            if self.field[x][y] == empty:
                return False
        return True

    def clear_completed(self):
        removed_lines = 0
        y = field_h - 1
        while y >= 0:
            if self.is_completed(y):
                for pushDownY in range(y, 0, -1):
                    for x in range(field_w):
                        self.field[x][pushDownY] = self.field[x][pushDownY - 1]
                for x in range(field_w):
                    self.field[x][0] = empty
                removed_lines += 1
            else:
                y -= 1
        return removed_lines

    def game_field(self, display_surf):
        pg.draw.rect(display_surf, (255, 255, 255),
                     (side_margin - 4, top_margin - 4, (field_w * Figure.block) + 8, (field_h * Figure.block) + 8), 5)

        pg.draw.rect(display_surf, (0, 0, 0), (side_margin, top_margin, Figure.block * field_w, Figure.block * field_h))
        for x in range(field_w):
            for y in range(field_h):
                fig = Figure.Figure(display_surf)
                fig.draw_block(x, y, self.field[x][y])
