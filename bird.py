from typing import Tuple, Literal
import pygame as pg
from config import *
from helper import image_loader


class Bird(pg.sprite.Sprite):
    """
    遊戲中的鳥(玩家)物件

    Attributes:
        y (float): 表示鳥頭頂(圖片上方)的垂直位置
        rotation_degree (float): 鳥的旋轉角度(degree), 逆時針為正
        image_index (0, 1, 2, 3): 鳥的圖片狀態(0-翅膀朝下, 1-翅膀置中, 2-翅膀朝上, 3-翅膀置中)
    Methods:
        move(): 處理鳥和移動(y座標)相關的更新
        update_image(): 處理鳥和圖片(圖片狀態, 旋轉角度)相關的更新
        update(): 處理鳥的所有更新
        draw(screen): 將鳥畫到視窗中
    """

    # TODO 額外的成員
    """
    _TODO2:
        Attributes:
            speed (float): 紀錄當前垂直速度
    _TODO4:
        Attributes:
            to_flap (int): 決定這一幀是否要拍動翅膀，每秒拍動約2次(每37/3=約12幀更新一次 -> to_flap == 12 時更新狀態)
            angular_velocity (float): 角速度，控制鳥的頭的旋轉速度
            max_degree (float): 鳥在移動時最高/低可以旋轉到幾度

    """


    images = [image_loader(path, (BIRD_WIDTH, BIRD_HEIGHT)) for path in BIRD_IMG_PATHS]

    def __init__(self, position: Tuple[float, float]):
        """
        初始化函式

        Args:
            position (Tuple[int, int]): 初始位置 (x, y), x 為鳥(圖片)左方的水平位置, y 為鳥(圖片)中心的垂直位置
        """
        pg.sprite.Sprite.__init__(self)
        self.image_index_ = 1
        self.image = Bird.images[self.image_index_]
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.rect.left = position[0]
        self.rotation_degree_ = 0
        
        #others attributes added
        self.speed = 0
        self.to_flap = 0
        self.max_degree = 30.0
        return

    def get_input(self) -> bool:  # 回傳滑鼠是否按下(True: 按下/False: 沒有按下)
        if pg.mouse.get_pressed()[0]:
            return True
        return False

    @property
    def y(self):
        return self.rect.top

    @y.setter
    def y(self, value: float):
        self.rect.top = value

    @property
    def rotation_degree(self):
        return self.rotation_degree_

    @rotation_degree.setter
    def rotation_degree(self, value: float):
        self.rotation_degree_ = value
        self.image = pg.transform.rotate(Bird.images[self.image_index_], self.rotation_degree_)

    @property
    def image_index(self):
        return self.image_index_

    @image_index.setter
    def image_index(self, value: Literal[0, 1, 2, 3]):
        self.image_index_ = value
        self.image = Bird.images[self.image_index_]

    # 處理鳥的移動
    def move(self):
        # TODO1&2 (5pts) 讓鳥(玩家)在接收到滑鼠點擊的訊號時，能向上移動，並讓鳥(玩家)在未接受到滑鼠點擊的訊號時，能向下移動
        # TODO1&2 (10pts) 讓鳥(玩家)在接收到單一次滑鼠點擊的訊號後，能"自然"移動
        if self.get_input():  # 當滑鼠點擊時條件為True, 反之為False
            acceleration = -0.3
        else:
            acceleration = 0.3
        
        self.speed += acceleration
        # TODO1&2 (5pts) 讓鳥(玩家)能夠垂直移動
        self.y += self.speed

    # 處理鳥的圖片設定(實現動畫)
    def update_image(self):
        # TODO4 讓鳥鳥更生動(增加動畫)

        #(5pts) 讓鳥(玩家)向上飛時略往上仰，向下墜時略往下看
        self.rotation_degree = -20
        if self.get_input():
            self.rotation_degree = 20

        
        #(5pts) 讓鳥(玩家)以合理的速率持續拍動翅膀
        if self.to_flap == 12:
            #switch back and forth between different state
            if self.image_index == 3:
                self.image_index = 0
            else:
                self.image_index += 1
            self.to_flap = 0
        else:
            self.to_flap += 1





    def update(self):
        self.update_image()
        self.move()
