import pygame
import random


class Game(object):
    def __init__(self):
        self.clock = pygame.time.Clock()  # для плавности
        self.screen = pygame.display.set_mode((640, 480))  # окно игры
        self.running = True  # работа игры

    def draw(self):
        pass

    def event_handler(self):
        pass

    def collision_check(self):
        pass