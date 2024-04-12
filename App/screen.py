import pygame
import random
from const import *


class Screen(object):
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)  # окно игры
        self.clock = pygame.time.Clock()  # для плавности

    def update(self):
        pygame.display.update()
        self.clock.tick(FPS)
