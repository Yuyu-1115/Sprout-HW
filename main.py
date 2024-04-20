import pygame as pg
from game import Game
from config import CAPTION, SCREEN_WIDTH, SCREEN_HEIGHT

if __name__ == "__main__":
    pg.init()
    pg.display.set_caption(CAPTION)
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    play_again = True
    game = Game(screen)
    while game.run():
        game = Game(screen)

    pg.quit()
