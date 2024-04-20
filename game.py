import pygame as pg
from pygame.constants import QUIT
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

    # TODO 額外的成員
    """
    _TODO7:
        Attributes:
            self.gameover_image (pg.Surface): Game Over圖片物件
            self.result_image (pg.Surface): 結算畫面背景物件(自己畫的)
            self.restart_image (pg.Surface): 結算畫面的重新開始按鈕物件(自己做的)
            self.quit_image (pg.Surface)結算畫面的離開按鈕物件(自己做的)
            self.restart_button (pg.Rect): 利用pg.Rect.collidepoint()達成按鈕功能
            self.quit_button (pg.Rect): 利用pg.Rect.collidepoint()達成按鈕功能
            self.highest_score (int): 歷史高分
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
        self.gameover_image = image_loader(
            GAMEOVER_IMG_PATH,(SCREEN_WIDTH / 2 + 100, SCREEN_WIDTH / 8)
        )
        self.result_image = image_loader(
            RESULT_IMG_PATH,(SCREEN_WIDTH - 200, SCREEN_WIDTH - 100)
        )

        #TODO (Extra) 在結算畫面提供重新開始和離開的按鈕
        self.restart_button = pg.Rect(100, 500, SCREEN_WIDTH / 4, SCREEN_WIDTH / 8)
        self.quit_button = pg.Rect(100 + SCREEN_WIDTH / 4, 500, SCREEN_WIDTH / 4, SCREEN_WIDTH / 8)

        self.restart_image = image_loader(
            RESTART_IMAGE_PATH, (SCREEN_WIDTH / 4, SCREEN_WIDTH / 8)
        )
        self.quit_image = image_loader(
            QUIT_IMAGE_PATH, (SCREEN_WIDTH / 4, SCREEN_WIDTH / 8)
        )


        #TODO (Extra) 透過檔案操作紀錄歷史最高分，儲存的部分在129行
        with open("record.txt", "r") as f:
            self.highest_score = int(f.read())


    # TODO7 讓遊戲流程更豐富
    def run(self):
        clock = pg.time.Clock()
        running = True
        base = pg.sprite.GroupSingle(Base())
        bird = pg.sprite.GroupSingle(Bird((SCREEN_WIDTH / 10, HEIGHT_LIMIT / 2)))
        pipes = Pipes()
        scoreboard = Scoreboard()
        started = False
        is_over = False

        # 畫背景、物件
        self.screen.blit(self.background_image, (0, 0))
        bird.draw(self.screen)
        pipes.draw(self.screen)
        base.draw(self.screen)
        scoreboard.draw(self.screen)
        pg.display.update()
        
        #TODO7 (5pts) 等待玩家第一次點擊才開始遊戲
        while not started:
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    started = True
                    break
                
        # game loop
        while running:
            clock.tick(FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT:  # "視窗關閉"事件
                    running = False

            if not is_over:
                # 更新遊戲
                base.update()
                bird.update()
                pipes.update(scoreboard.score)
                scoreboard.update(pipes.is_passed)

            ## 遊戲結束與否
            ### 碰撞發生 或 超出螢幕範圍
            if pg.sprite.groupcollide(bird, pipes.pipes, False, False):
                is_over = True
            

            # 畫背景、物件
            self.screen.blit(self.background_image, (0, 0))
            bird.draw(self.screen)
            pipes.draw(self.screen)
            base.draw(self.screen)
            scoreboard.draw(self.screen)

            if is_over:
                # TODO7 (Option 1 5pts) 結束時顯示 Game Over 提示語並顯示得分
                # TODO7 (Extra 5pts) 歷史分數紀錄

                # 更新最高分並儲存於record.txt
                self.highest_score = max(self.highest_score, scoreboard.score)
                with open("record.txt", "w") as f:
                    f.write(str(self.highest_score))
                
                # 顯示結算畫面
                self.screen.blit(self.result_image, (100, 200))
                scoreboard.result(self.screen, self.highest_score)
                self.screen.blit(self.gameover_image, (SCREEN_WIDTH / 4 - 50, 165))
                self.screen.blit(self.restart_image, (100, 500))
                self.screen.blit(self.quit_image, (230, 500))
                
                #TODO7 (Option 2 5pts) 遊戲結束後，讓玩家能按任意鍵重新開始遊戲
                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if self.restart_button.collidepoint(pg.mouse.get_pos()):
                            return True
                        if self.quit_button.collidepoint(pg.mouse.get_pos()):
                            return False
                        

            pg.display.update()



            
