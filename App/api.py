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
        return [self.is_near(coords, walls, '+x'), self.is_near(coords, walls, '-x'), self.is_near(coords, walls, '+y'), self.is_near(coords, walls, '-y')]

    def is_near (self, coords, walls, type):
        snake_head = coords[-1]
        if (type == '-x'):
            next = [snake_head[0] - 1, snake_head[1]]
            return ((next in coords) or next == [0, snake_head[1]])
        elif (type == '+x'):
            next = [snake_head[0] + 1, snake_head[1]]
            return ((next in coords) or next == [walls[0][1], snake_head[1]])
        elif (type == '+y'):
            next = [snake_head[0], snake_head[1] - 1]
            return ((next in coords) or next == [snake_head[0], 0])
        elif (type == '-y'):
            next = [snake_head[0], snake_head[1] + 1]
            return ((next in coords) or next == [snake_head[0], walls[1][1]])

    def update(self, coords, food):
        pass