import pygame
import random
from const import *


class Api(object):
    def __init__(self):
        self.step = SNAKE_STEP  # размер сетки

    def snake_to_food(self, coords, food):
        coords=coords[-1]
        one = coords[0] - food[0]
        two = coords[1] - food[1]
        return (one, two)

    def is_near_obs (self, coords):
        snake_head = coords[-1]
        x_right=[snake_head[0]+1, snake_head[1]]
        x_left = [snake_head[0] -1, snake_head[1]]
        y_up = [snake_head[0], snake_head[1]-1]
        y_down = [snake_head[0], snake_head[1]+1]

        return [(x_right in coords), (x_left in coords), (y_up in coords), (y_down in coords)]