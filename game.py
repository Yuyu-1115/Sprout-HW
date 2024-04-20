import pygame as pg
from config import *
from helper import image_loader

from base import Base
from bird import Bird
from pipe import Pipes
from scoreboard import Scoreboard


class Game:
    """
    遊戲控制物件

    Attributes:
        screen (pg.Surface): 視窗物件
        background_image (pg.Surface): 背景圖片物件
    Methods:
        run(): 開始遊戲(進入遊戲迴圈)
    """

    def __init__(self, surface: pg.surface):
        """
        初始化函式

        Args:
            surface (pg.surface): 視窗物件
        """
        self.screen = surface
        self.background_image = image_loader(
            BACKGROUND_IMG_PATH, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

    # TODO7 讓遊戲流程更豐富
    def run(self):
        clock = pg.time.Clock()
        running = True
        base = pg.sprite.GroupSingle(Base())
        bird = pg.sprite.GroupSingle(Bird((SCREEN_WIDTH / 10, HEIGHT_LIMIT / 2)))
        pipes = Pipes()
        scoreboard = Scoreboard()
        started = False

        # game loop
        while running:
            clock.tick(FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT:  # "視窗關閉"事件
                    running = False

            # 更新遊戲
            base.update()
            bird.update()
            pipes.update()
            scoreboard.update(pipes.is_passed)

            ## 遊戲結束與否
            ### 碰撞發生
            if pg.sprite.groupcollide(bird, pipes.pipes, False, False):
                running = False

            # 畫背景、物件
            self.screen.blit(self.background_image, (0, 0))
            bird.draw(self.screen)
            pipes.draw(self.screen)
            base.draw(self.screen)
            scoreboard.draw(self.screen)
            pg.display.update()

            
