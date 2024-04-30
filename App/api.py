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