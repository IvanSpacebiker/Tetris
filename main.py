import pygame as pg
import Game

pg.init()
game = Game.Game()
pg.display.set_caption('Tetris')
game.show_text('Tetris')
while True:
    game.run_tetris()
    game.pause_screen()
    game.show_text('Game over')
