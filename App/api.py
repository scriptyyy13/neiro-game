import pygame
import random
from const import *


class Api(object):
    def __init__(self):
        self.step = SNAKE_STEP  # размер сетки
        self.coords = []
        self.walls = ((0, 0), (0, 0))

    def snake_to_food(self, coords, food):
        coords = coords[-1]
        one = coords[0] - food[0]
        two = coords[1] - food[1]
        return (one, two)

    def is_near_obs(self, coords, walls):
        snake_head = coords[-1]
        return [self.is_near_px(coords, walls), self.is_near_mx(coords, walls), self.is_near_py(coords, walls), self.is_near_my(coords, walls)]

    def is_near_px(self, coords, walls):
        snake_head = coords[-1]
        next = [snake_head[0] + 1, snake_head[1]]
        return ((next in coords) or next == [walls[0][1], snake_head[1]])

    def is_near_mx(self, coords, walls):
        snake_head = coords[-1]
        next = [snake_head[0] - 1, snake_head[1]]
        return ((next in coords) or next == [0, snake_head[1]])

    def is_near_py(self, coords, walls):
        snake_head = coords[-1]
        next = [snake_head[0], snake_head[1] - 1]
        return ((next in coords) or next == [snake_head[0], 0])

    def is_near_my(self, coords, walls):
        snake_head = coords[-1]
        next = [snake_head[0], snake_head[1] + 1]
        return ((next in coords) or next == [snake_head[0], walls[1][1]])


    def update(self, coords, food):
        pass