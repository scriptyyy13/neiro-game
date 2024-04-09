from typing import List

import pygame
import random


class Snake(object):
    def __init__(self):
        self.length = 1 # начальная длина
        self.vector = (0, 1)  # начальный вектор движения
        self.speed = 1 # увеличение скорости
        self.coords = [[0, 0]] # координаты всех частей змейки

    def set_vector(self):
        pass

    def update(self):
        pass
