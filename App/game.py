import pygame
import random
from screen import *
from snake import *
from food import *
from board import *
from const import *


class Game(object):
    def __init__(self):
        self.running = True  # работа игры
        self.screen = Screen()  # создаем окно игры
        self.board = Board()  # создаем окно игры
        self.snake = Snake()  # змейка
        self.food = Food()  # еда змейки

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.event_handler(event)
            self.snake.update()
            if (self.snake.coords[-1][0] == self.food.food_pos[0] and self.snake.coords[-1][1] == self.food.food_pos[1]):
                self.snake.length += 1 # увеличиваем на 1 змейку, при поедании еды
            self.food.update(self.snake.coords)
            self.draw()

    def draw(self):
        self.screen.screen.fill(WHITE)
        self.board.draw(self.screen.screen)
        self.snake.draw_snake(self.snake.coords, self.screen.screen)
        self.food.draw(self.screen.screen)
        self.screen.update()

    def update(self):
        pass

    def event_handler(self, event):
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.KEYDOWN:  # управление змейкой
            if event.key == pygame.K_w and self.snake.vector[1] == 0:
                self.snake.vector = (0, -1)
            elif event.key == pygame.K_a and self.snake.vector[0] == 0:
                self.snake.vector = (-1, 0)
            elif event.key == pygame.K_s and self.snake.vector[1] == 0:
                self.snake.vector = (0, 1)
            elif event.key == pygame.K_d and self.snake.vector[0] == 0:
                self.snake.vector = (1, 0)

    def collision_check(self):
        pass


if __name__ == '__main__':
    game = Game()
    game.run()
