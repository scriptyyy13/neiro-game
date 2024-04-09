from typing import List

import pygame
import random


class Screen(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((640, 480))  # окно игры

    def update(self):
        pass
