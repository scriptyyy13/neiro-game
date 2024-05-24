import pygame
import random

from screen import *
from snake import *
from food import *
from board import *
from api import *
from const import *
from Neural.neural_network import *

pygame.font.init()

class Game(object):
    def __init__(self):
        self.running = True  # работа игры
        self.screen = Screen()  # создаем окно игры
        self.board = Board()  # создаем окно игры
        self.snake = Snake()  # змейка
        self.food = Food()  # еда змейки
        self.api = Api()  # апи
        self.neiro = Neiro()  # нейронка
        self.font = pygame.font.SysFont('MS Gothic', 30) # шрифт
        self.best_score = 0 # лучший счет

    def run(self):
        self.api.update(self.snake.coords, self.food.food_pos, (self.board.get_wall_x(), self.board.get_wall_y()))
        while self.running:
            for event in pygame.event.get():
                self.event_handler(event)

            self.update()

            if (self.snake.score > self.best_score):
                self.best_score = self.snake.score

            self.draw()

    def draw(self):
        self.screen.screen.fill(WHITE)
        self.board.draw(self.screen.screen)
        self.snake.draw_snake(self.snake.coords, self.screen.screen)
        self.food.draw(self.screen.screen)
        text_surface = self.font.render(str(self.snake.score), False, (0, 0, 0))
        self.screen.screen.blit(text_surface, (40, 400))
        text_surface1 = self.font.render(str(self.best_score), False, (0, 0, 0))
        self.screen.screen.blit(text_surface1, (40, 430))
        self.screen.update()

    def update(self):
        self.food.update(self.snake.coords)
        self.api.update(self.snake.coords, self.food.food_pos, (self.board.get_wall_x(), self.board.get_wall_y()))

        if (SNAKE_AUTO == 1):
            self.snake.auto_hodilka(self.api.snake_to_food())
        elif (SNAKE_AUTO == 2):
            data=self.api.is_near_obs()
            for i in range(4):
                if (data[i] == True):
                    data[i]=1
                else:
                    data[i]=0
            data.append(self.snake.length)
            data.append(self.api.snake_to_food())
            where_to_go = self.neiro.run(data)
            max_index = 0
            maxi = 0
            for j in range(4):
                if (where_to_go[j] > maxi):
                    maxi = where_to_go[j]
                    max_index = j
            print(where_to_go, self.api.snake_to_food())
            if max_index == 2 and self.snake.vector[1] == 0:
                self.snake.vector = (0, -1)
            elif max_index == 1 and self.snake.vector[0] == 0:
                self.snake.vector = (-1, 0)
            elif max_index == 3 and self.snake.vector[1] == 0:
                self.snake.vector = (0, 1)
            elif max_index == 0 and self.snake.vector[0] == 0:
                self.snake.vector = (1, 0)

        self.snake.update()
        self.collision_check()
        self.neiro.learn(self.api.snake_to_food(), self.snake.length)

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
        if (self.board.get_wall_x()[0] == self.snake.coords[-1][0] or self.board.get_wall_x()[1] ==
                self.snake.coords[-1][0]):
            self.snake.snake_reset()  # ресет змейки при врезании в стены по бокам
        if (self.board.get_wall_y()[0] == self.snake.coords[-1][1] or self.board.get_wall_y()[1] ==
                self.snake.coords[-1][1]):
            self.snake.snake_reset()  # ресет змейки при врезании в стены сверху и снизу

        if (self.snake.coords[-1][0] == self.food.food_pos[0] and self.snake.coords[-1][1] == self.food.food_pos[1]):
            self.snake.length += 1  # увеличиваем на 1 змейку, при поедании еды
            self.snake.score += 1


if __name__ == '__main__':
    game = Game()
    game.run()
