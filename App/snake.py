import pygame
import random
from const import *


class Snake(object):
    def __init__(self):
        self.length = SNAKE_START_LENGHT  # начальная длина
        self.vector = SNAKE_START_VECTOR  # начальный вектор движения
        self.speed = SNAKE_SPEED_MULTIPLIER  # увеличение скорости
        self.coords = [[0, 0]]  # координаты головы

    def set_vector(self):
        pass

    def update(self):
        pass

