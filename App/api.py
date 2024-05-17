import pygame
import random
from const import *


class Api(object):
    def __init__(self):
        self.step = SNAKE_STEP  # размер сетки
        self.coords = []
        self.walls = ((0, 0), (0, 0))
        self.food = (0, 0)

    def snake_to_food(self):
        self.coords1 = self.coords[-1]
        one = self.coords1[0] - self.food[0]
        two = self.coords1[1] - self.food[1]
        return abs(one+two)

    def is_near_obs(self):
        return [self.is_near_px(), self.is_near_mx(), self.is_near_py(), self.is_near_my()]

    def is_near_px(self):
        snake_head = self.coords[-1]
        next = [snake_head[0] + 1, snake_head[1]]
        return ((next in self.coords) or next == [self.walls[0][1], snake_head[1]])

    def is_near_mx(self):
        snake_head = self.coords[-1]
        next = [snake_head[0] - 1, snake_head[1]]
        return ((next in self.coords) or next == [0, snake_head[1]])

    def is_near_py(self):
        snake_head = self.coords[-1]
        next = [snake_head[0], snake_head[1] - 1]
        return ((next in self.coords) or next == [snake_head[0], 0])

    def is_near_my(self):
        snake_head = self.coords[-1]
        next = [snake_head[0], snake_head[1] + 1]
        return ((next in self.coords) or next == [snake_head[0], self.walls[1][1]])

    def update(self, coords, food, walls):
        self.coords = coords
        self.food = food
        self.walls = walls