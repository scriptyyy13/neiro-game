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
        self.snake.draw_snake(self.snake.coords, self.screen.screen)
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
