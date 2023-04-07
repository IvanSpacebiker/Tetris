import sys
import time

import pygame as pg
from pygame.locals import *

import Field
import Figure
from Figure import Figure as Fig
from Field import Field as Fie

fps = 25
window_w, window_h = 600, 500
side_freq, down_freq = 0.15, 0.1


class Game:

    def __init__(self):
        self.field = None
        self.surface = pg.display.set_mode((window_w, window_h))
        self.fps = pg.time.Clock()
        self.fonts = [pg.font.SysFont('consolas', 20), pg.font.SysFont('consolas', 45)]

    def run_tetris(self):
        self.field = Fie()
        last_move_down = time.time()
        last_side_move = time.time()
        last_fall = time.time()
        going_down = False
        going_left = False
        going_right = False
        points = 0
        level, fall_speed = self.calc_speed(points)
        fallingFig = Fig(self.surface)
        nextFig = Fig(self.surface)

        while True:
            if fallingFig == None:
                fallingFig = nextFig
                nextFig = Fig(self.surface)
                last_fall = time.time()

                if not self.field.check_pos(fallingFig):
                    return

            for event in pg.event.get():
                if event.type == QUIT or event.type == KEYUP and event.key == K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.type == KEYUP:
                    if event.key == K_SPACE:
                        self.pause_screen()
                        self.show_text('Pause')
                        last_fall = time.time()
                        last_move_down = time.time()
                        last_side_move = time.time()
                    elif event.key == K_LEFT:
                        going_left = False
                    elif event.key == K_RIGHT:
                        going_right = False
                    elif event.key == K_DOWN:
                        going_down = False

                elif event.type == KEYDOWN:

                    if event.key == K_LEFT and self.field.check_pos(fallingFig, adjX=-1):
                        fallingFig.x -= 1
                        going_left = True
                        going_right = False
                        last_side_move = time.time()

                    elif event.key == K_RIGHT and self.field.check_pos(fallingFig, adjX=1):
                        fallingFig.x += 1
                        going_right = True
                        going_left = False
                        last_side_move = time.time()

                    elif event.key == K_UP:
                        fallingFig.rotation = (fallingFig.rotation + 1) % len(Figure.figures[fallingFig.shape])
                        if not self.field.check_pos(fallingFig):
                            fallingFig.rotation = (fallingFig.rotation - 1) % len(
                                Figure.figures[fallingFig.shape])

                    elif event.key == K_DOWN:
                        going_down = True
                        if self.field.check_pos(fallingFig, adjY=1):
                            fallingFig.y += 1
                        last_move_down = time.time()

                    elif event.key == K_RETURN:
                        going_down = False
                        going_left = False
                        going_right = False
                        for i in range(1, Field.field_h):
                            if not self.field.check_pos(fallingFig, adjY=i):
                                break
                        fallingFig.y += i - 1

                    elif event.key == K_r:
                        self.run_tetris()

            if (going_left or going_right) and time.time() - last_side_move > side_freq:
                if going_left and self.field.check_pos(fallingFig, adjX=-1):
                    fallingFig.x -= 1
                elif going_right and self.field.check_pos(fallingFig, adjX=1):
                    fallingFig.x += 1
                last_side_move = time.time()

            if going_down and time.time() - last_move_down > down_freq and self.field.check_pos(fallingFig, adjY=1):
                fallingFig.y += 1
                last_move_down = time.time()

            if time.time() - last_fall > fall_speed:
                if not self.field.check_pos(fallingFig, adjY=1):
                    self.field.add_to_cup(fallingFig)
                    add_points = self.field.clear_completed()
                    points += add_points * 4 if add_points == 4 else add_points
                    level, fall_speed = self.calc_speed(points)
                    fallingFig = None
                else:
                    fallingFig.y += 1
                    last_fall = time.time()

            self.surface.fill((0, 0, 0))
            self.draw_title()
            self.field.game_field(self.surface)
            self.draw_info(points, level)

            if fallingFig != None:
                fallingFig.draw_fig()
            pg.display.update()
            self.fps.tick(fps)

    def pause_screen(self):
        pause = pg.Surface((600, 500), pg.SRCALPHA)
        pause.fill((0, 0, 255, 127))
        self.surface.blit(pause, (0, 0))

    def txt_objects(self, text, font, color):
        surf = font.render(text, True, color)
        return surf, surf.get_rect()

    def show_text(self, text):
        titleSurf, titleRect = self.txt_objects(text, self.fonts[1], (225, 225, 0))
        titleRect.center = (int(window_w / 2) - 3, int(window_h / 2) - 3)
        self.surface.blit(titleSurf, titleRect)

        pressKeySurf, pressKeyRect = self.txt_objects('Press any key', self.fonts[0],
                                                      (225, 225, 0))
        pressKeyRect.center = (int(window_w / 2), int(window_h / 2) + 100)
        self.surface.blit(pressKeySurf, pressKeyRect)

        while self.check_keys() is None:
            pg.display.update()
            self.fps.tick()

    def check_keys(self):
        for event in pg.event.get([KEYDOWN, KEYUP]):
            if event.type == KEYDOWN:
                continue
            return event.key
        return None

    def draw_title(self):
        titleSurf = self.fonts[1].render('Tetris', True, (225, 225, 0))
        titleRect = titleSurf.get_rect()
        titleRect.topleft = (window_w - 360, 30)
        self.surface.blit(titleSurf, titleRect)

    def draw_info(self, points, level):
        pointsSurf = self.fonts[0].render(f'Points: {points}', True, (255, 255, 255))
        pointsRect = pointsSurf.get_rect()
        pointsRect.topleft = (window_w - 170, 100)
        self.surface.blit(pointsSurf, pointsRect)

        levelSurf = self.fonts[0].render(f'Level: {level}', True, (255, 255, 255))
        levelRect = levelSurf.get_rect()
        levelRect.topleft = (window_w - 170, 130)
        self.surface.blit(levelSurf, levelRect)

    def calc_speed(self, points):
        level = int(points / 10) + 1
        fall_speed = 0.27 - (level * 0.02)
        return level, fall_speed
