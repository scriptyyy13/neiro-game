import pygame
import random
from const import *


class Snake(object):
    def __init__(self):
        self.length = SNAKE_START_LENGHT  # начальная длина
        self.vector = SNAKE_START_VECTOR  # начальный вектор движения
        self.speed = SNAKE_SPEED_MULTIPLIER  # увеличение скорости
        self.coords = [[128, 300]]  # координаты головы

    def set_vector(self):
        pass

    def update(self):
        if (self.length < len(self.coords)):
            pass

    def draw_snake(self, coords, screen):
        for i in range(len(coords)):
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(coords[i][0], coords[i][1], 30, 30))

