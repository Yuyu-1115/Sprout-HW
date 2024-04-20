from typing import Tuple, Literal
import pygame as pg
from config import *
from helper import image_loader, MyList
import random


# a single pipe
class Pipe(pg.sprite.Sprite):
    """
    遊戲中的單一根水管物件

    Attributes:
        direction ("UP", "DOWN"): 表示水管開口的方向
        x (float): 表示水管(圖片)左方的水平座標
        y (float): 表示水管"開口"的垂直位置(開口朝上則為圖片最上方, 開口朝下則為圖片最下方)
    Methods:
        update(): 處理水管的位置更新
        draw(screen): 將水管畫到視窗中
    """

    img = image_loader(PIPE_IMG_PATH, (PIPE_WIDTH, PIPE_HEIGHT))
    flipped_img = pg.transform.flip(img, False, True)

    def __init__(self, position: Tuple[float, float], direction: Literal["UP", "DOWN"]):
        """
        初始化函式

        Args:
            position (Tuple[int, int]): 初始位置 (x, y), x 為水管(圖片)左方的水平位置, y 為水管(圖片)開口的垂直位置
            init_value (0, 1, 2, 3, 4, 5, 6, 7, 8, 9): 初始數字
        """
        pg.sprite.Sprite.__init__(self)
        self.direction = direction
        if self.direction == "DOWN":  # 上面(管口朝下)
            self.image = Pipe.flipped_img
            self.rect = self.image.get_rect()
            self.rect.bottomleft = position
        else:  # 下面(管口朝上)
            self.image = Pipe.img
            self.rect = self.image.get_rect()
            self.rect.topleft = position

    @property
    def x(self):
        return self.rect.left

    @x.setter
    def x(self, value):
        self.rect.left = value

    @property
    def y(self):
        if self.direction == "UP":
            return self.rect.top
        else:
            return self.rect.bottom

    @y.setter
    def y(self, value):
        if self.direction == "UP":
            self.rect.top = value
        else:
            self.rect.bottom = value

    def update(self):
        self.x -= BASE_SCROLLING_SPEED
        if self.x + PIPE_WIDTH < 0:
            self.kill()


# an upper pipe and a lower pipe
class PipePair:
    """
    遊戲中的一對(上下兩根)水管物件

    Attributes:
        bottom_pipe (Pipe): 底下的水管
        top_pipe (Pipe): 上方的水管
        x (float): 兩根水管左方的水平座標
    Methods:
        update(): 更新這一對水管的位置
        draw(screen): 將這一對水管畫到視窗中
        is_alive() -> bool: 回傳這一對水管是否還需要更新(存在於視窗中)
    """



    def __init__(self):
        # TODO5 讓每次新增的 Pipe_pair 略有不同 !
        """
        透過 random library 來輔助達成目標
        """
        # -----------------以下要修改----------------- #

        pipe_gap = random.randint(100, 300)
        center = HEIGHT_LIMIT / 2 + random.randint(-150, 150)
        pipe_top = Pipe((SCREEN_WIDTH, center - (pipe_gap / 2)), "DOWN")
        pipe_btm = Pipe((SCREEN_WIDTH, center + (pipe_gap / 2)), "UP")

        # -----------------以上要修改----------------- #

        self.pipes = pg.sprite.Group()
        self.pipes.add(pipe_btm), self.pipes.add(pipe_top)


    @property
    def bottom_pipe(self):
        return self.pipes.sprites()[0]

    @property
    def top_pipe(self):
        return self.pipes.sprites()[1]

    @property
    def x(self):
        return self.bottom_pipe.x

    def update(self) -> bool:
        self.pipes.update()

    def draw(self, screen: pg.surface):
        self.pipes.draw(screen)

    def is_alive(self) -> bool:  # 回傳此 pipe_pair 是否還存活在 window 中，即仍需要被更新
        if len(self.pipes) == 0:
            return False
        return True


# all pipes
class Pipes:
    """
    遊戲中控制所有水管的物件

    Attributes:
        pipes_counter (int): 已經產生的水管對數
        pipe_pairs (MyList[PipePair]): 所有在視窗中的水管對
        pipes (pg.sprite.Group): 所有在視窗中的水管
    Methods:
        add_pipe(): 新增一對水管對(在視窗的最右方)
        update(): 更新所有水管對的狀態(位置, 不存在視窗中的水管對移除, 新增新的水管對)
        draw(): 將所有水管對畫到視窗中
    """

    #extra things added
    """
    TODO3:
        Attributes:
            frame (int): 顯示當前處於第幾幀，用於控制水管的生成
    TODO6:
        Attributes:
            is_passed (boolean): 當前幀是否有鳥通過水管
    """

    def __init__(self):
        self.pipes_counter = 0
        self.pipe_pairs = MyList()

        #extra attributes added
        self.frame = 0
        self.is_passed = False

    @property
    def pipes(self):
        re = pg.sprite.Group()
        cursor = self.pipe_pairs.head
        while cursor != None:
            sprites = cursor.data.pipes.sprites()
            re.add(sprites[0]), re.add(sprites[1])
            cursor = cursor.nxt
        return re

    def add_pipe(self):
        self.pipes_counter += 1
        self.pipe_pairs.push_back(PipePair())

    def update(self):
        # 更新所有水管
        # is_passed 水管是否經過鳥了
        self.is_passed = False
        cursor = self.pipe_pairs.head
        while cursor != None:
            cursor.data.update()
            cursor = cursor.nxt

        # 刪除已經超出螢幕的水管
        cursor = self.pipe_pairs.peek()
        while cursor != None and not cursor.is_alive():
            self.pipe_pairs.pop_top()
            cursor = self.pipe_pairs.peek()
            self.is_passed = True

        # TODO3 (Done)決定何時新增水管
        self.frame += 1
        if self.frame > (FPS):
            self.frame = 1
        # 每N幀新增一個水管
        if self.frame % (FPS) == 0 :
            self.add_pipe()

        """
        控制這次更新需不需要新增水管
        呼叫self.add_pipe()即會新增一對水管對
        """
        # FIXME (Done)取消下行的註解看看不做控制直接新增會發生什麼事
        #self.add_pipe()

    def draw(self, screen: pg.surface):
        cursor = self.pipe_pairs.head
        while cursor != None:
            cursor.data.draw(screen)
            cursor = cursor.nxt


# TODO8 過動的水管
"""
可以直接修改, 也可以透過繼承 Pipe, PipePair 創造不同行為的水管
"""
