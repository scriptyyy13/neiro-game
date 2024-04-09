import pygame
import random
from screen import *
from snake import *
from const import *


class Game(object):
    def __init__(self):
        self.running = True  # работа игры
        self.screen = Screen()  # создаем окно игры
        self.snake = Snake() # змейка

    def run(self):
        while self.running:
            self.draw()

    def draw(self):
        self.screen.screen.fill(WHITE)
        # pygame.draw.rect(self.screen.screen, (0,0,0), pygame.Rect(30, 30, 60, 60))

        self.screen.update()

    def update(self):
        pass

    def event_handler(self):
        pass

    def collision_check(self):
        pass


if __name__ == '__main__':
    game = Game()
    game.run()
