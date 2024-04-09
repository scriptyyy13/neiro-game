import pygame
import random
from screen import *


class Game(object):
    def __init__(self):
        self.clock = pygame.time.Clock()  # для плавности
        self.running = True  # работа игры

    def run(self):
        pass

    def draw(self):
        pass

    def event_handler(self):
        pass

    def collision_check(self):
        pass

if __name__ == '__main__':
    game = Game()
    screen = Screen()
    while game.running:
        a = 1
