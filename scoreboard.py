from typing import Tuple
import pygame as pg
from number import Number
from config import SCREEN_WIDTH, NUMBER_WIDTH, FONT_PATH
from math import log10

# TODO6 完成記分板物件
"""
記分板物件需至少支援三個方法
1. __init__(): constructor, 用來建構一個記分板物件實體
2. update(): 用來作為遊戲迴圈中每次更新呼叫的更新函式, 更新記分板物件中的邏輯部分(分數部分)
3. draw(screen): 遊戲迴圈更新後將記分板畫到視窗中的函式
"""

"""
hint: 可以利用實作好的Number物件幫忙
"""

# TODO 額外的成員
"""
_TODO6:
    Attributes:
        score(int): 分數
        number_list(list(Number)): 分數的list, number_list[0]為首位數
        power(int): 分數的位數(10的冪次)
    Methods:
        carry(index): 處理進位時數字的顯示
        reposition(): 讓數字能夠對稱(強迫症)
_TODO7:
    Attributes:
        font(pg.font.Font): 分數顯示及按鈕的字體 (Credit: https://github.com/ACh-K/Cubic-11)
    Methods:
        result(screen: pg.Surface, highest_socre: int): 結算畫面顯示(文字及分數部分)

"""


class Scoreboard:
    def __init__(self):
        self.score = 0
        self.number_list = [Number((SCREEN_WIDTH / 2 - NUMBER_WIDTH / 2, 100), 0)]
        self.power = 0
        self.font = pg.font.Font(FONT_PATH, 30)


    def update(self, is_passed):
        if is_passed:
            self.score += 1
            if self.score % 10 == 0 and self.score != 0:
                self.carry(self.power)
            else:
                self.number_list[self.power].number += 1
            
    
    #TODO (Extra?) 我不確定這個部份(carry()跟reposition()算不算就是了
    def carry(self, index):
        # Case 1: 9要進位為10
        if self.score == 10:
            self.power += 1
            self.number_list.append(Number((SCREEN_WIDTH / 2 + NUMBER_WIDTH / 2, 100), 0))
            self.number_list[0].number = 1
            self.reposition(self.number_list)
        # Case 2: 被進位的那位是9
        elif self.number_list[index - 1].number == 9:
            # Case 2.a: 需要追加位數 e.g. [9, 9], [9, 9, 9]
            if (index - 1) == 0:
                self.power += 1
                for number in self.number_list:
                    number.number = 0
                self.number_list.append(Number((SCREEN_WIDTH / 2 + (NUMBER_WIDTH / 2) * self.power, 100), 0))
                self.number_list[0].number = 1
                self.reposition(self.number_list)
            # Case 2.b: 不需要追加位數，但會再牽扯到前一位 e.g. [1, 0, 9, 9]
            else:
                self.carry(index - 1)
                self.number_list[index].number = 0
        # Case 3: 被進位的那位不是9 e.g. [1, 9], [2, 9]
        else:
            self.number_list[index - 1].number += 1
            self.number_list[index].number = 0
    
    def reposition(self, number_list):
        #將所有Number向左平移半長度，達成左右對稱的效果
        for i in range(len(number_list)):
            number = number_list[i]
            number_list[i] = Number((number.position[0] - NUMBER_WIDTH / 2, number.position[1]), number.number)


    def draw(self, screen: pg.Surface):
        #TODO6 (5pts) 在視窗中間偏上的位置顯示出數字表示得分
        for number in self.number_list:
            number.draw(screen)

    def result(self, screen: pg.Surface, highest_score):
        screen.blit(self.font.render("Score:", True, 255), (150, 230))
        #顯示本局分數
        for i in range(0, self.power + 1):
            number = self.number_list[i]
            Number((number.position[0], 280), number.number).draw(screen)
        
        #顯示歷史紀錄
        screen.blit(self.font.render("Highest:", True, 255), (150, 350))

        #取得最高分的位數
        if highest_score > 0:
            power = int(log10(highest_score))
        else:
            power = 0
        
        #將分數轉換成list[Number]的表示方式再做顯示
        highest_number = []
        for i in range(power + 1):
            highest_number.append(Number((SCREEN_WIDTH / 2 + (NUMBER_WIDTH / 2) * i, 400), int(str(highest_score)[i])))
            self.reposition(highest_number)
        for number in highest_number:
            number.draw(screen)
            