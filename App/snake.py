import pygame
import random
from const import *


class Snake(object):
    def __init__(self):
        self.length = SNAKE_START_LENGHT  # начальная длина
        self.vector = SNAKE_START_VECTOR  # начальный вектор движения
        self.speed = SNAKE_SPEED_MULTIPLIER  # увеличение скорости
        self.step = SNAKE_STEP  # размер сетки змейки
        self.coords = [[5, 9]]  # координаты головы
        self.score = 0 # счет

    def snake_reset(self):
        self.length = SNAKE_START_LENGHT
        self.vector = SNAKE_START_VECTOR
        self.coords = [[5, 9]]
        self.score = 0

    def update(self):
        new_pice = [self.coords[-1][0]+self.vector[0], self.coords[-1][1]+self.vector[1]]  # создание след. кусочка змейки
        if (self.length == len(self.coords)):
            del self.coords[0] # удаление предыдущего кусочка змейки
        if (new_pice not in self.coords): # если там нет змейки, то все ок
            self.coords.append(new_pice)
        else: # сброс змейки при врезании в себя
            self.snake_reset()

    def draw_snake(self, coords, screen):
        for i in range(len(coords)):
            pygame.draw.rect(screen, (0, 0, 0), # отрисовка кусочков змейки
                             pygame.Rect(coords[i][0] * self.step, coords[i][1] * self.step, self.step, self.step))

    def auto_hodilka (self, where):
        if (where[0] == False):
            self.vector = (-1, 0)
        if (where[0]  == False):
            self.vector = (1, 0)
        if (where[1]  == False):
            self.vector = (0, -1)
        if (where[1]  == False):
             self.vector = (0, 1)
