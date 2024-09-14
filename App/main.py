import pygame
import random
import logging

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
        self.ndbr = 0 # нужность ресета
        self.model_number = 0 # номер модели
        self.logs = logging.basicConfig(level=logging.INFO, filename="../Saves/snake.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

    def run(self): # основная функция
        self.api.update(self.snake.coords, self.food.food_pos, (self.board.get_wall_x(), self.board.get_wall_y())) # первая передача данных в апи
        while self.running:
            for event in pygame.event.get(): # обработчик событий
                self.event_handler(event)
            self.update() # запускаем обновление

            if (self.snake.score > self.best_score): # обновление счета
                self.best_score = self.snake.score
                logging.info(f"Новый лучший счет: {str(self.best_score)}")

            self.draw() # вызов отрисовщика

    def draw(self): # отрисовка
        self.screen.screen.fill(WHITE)  # белый фон
        self.board.draw(self.screen.screen) # рисуем границы
        self.snake.draw_snake(self.snake.coords, self.screen.screen) # рисуем змейку
        self.food.draw(self.screen.screen) # рисуем еду
        text_surface = self.font.render(str(self.snake.score), False, (0, 0, 0)) # счет
        self.screen.screen.blit(text_surface, (40, 400))
        text_surface1 = self.font.render(str(self.best_score), False, (0, 0, 0)) # лучший счет
        self.screen.screen.blit(text_surface1, (40, 430))
        self.screen.update() # обновляем кадр

    def update(self):
        self.food.update(self.snake.coords, self.ndbr) # обновляем еду
        self.ndbr = 0
        self.api.update(self.snake.coords, self.food.food_pos, (self.board.get_wall_x(), self.board.get_wall_y())) # обновляем апи

        if (SNAKE_AUTO == 2): # отправляем инфу в нейронку
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
            if max_index == 2 and self.snake.vector[1] == 0:
                self.snake.vector = (0, -1)
            elif max_index == 1 and self.snake.vector[0] == 0:
                self.snake.vector = (-1, 0)
            elif max_index == 3 and self.snake.vector[1] == 0:
                self.snake.vector = (0, 1)
            elif max_index == 0 and self.snake.vector[0] == 0:
                self.snake.vector = (1, 0)

        self.neiro.learn(self.api.snake_to_food(), self.snake.length, self.snake.coords, self.food.food_pos, self.api.is_near_obs()) # обучение нейронки
        self.snake.update() # обновляем змейку
        self.collision_check() # проверка коллизий

    def event_handler(self, event): # события
        if event.type == pygame.QUIT: # выход из игры
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
            elif event.key == pygame.K_r: # сохранение нынешней нейронки
                self.neiro.save(self.model_number)
                logging.info(f"Сохранено {self.model_number}")
            elif event.key == pygame.K_t: # прочтение последнего сохранения
                self.neiro.read(self.model_number)
                logging.info(f"Сохранение прочитано {self.model_number}")

    def collision_check(self): # проверка коллизий
        if (self.board.get_wall_x()[0] == self.snake.coords[-1][0] or self.board.get_wall_x()[1] ==
                self.snake.coords[-1][0]):
            self.snake.snake_reset()  # ресет змейки при врезании в стены по бокам
            self.ndbr = 1
        if (self.board.get_wall_y()[0] == self.snake.coords[-1][1] or self.board.get_wall_y()[1] ==
                self.snake.coords[-1][1]):
            self.snake.snake_reset()  # ресет змейки при врезании в стены сверху и снизу
            self.ndbr = 1

        if (self.snake.coords[-1][0] == self.food.food_pos[0] and self.snake.coords[-1][1] == self.food.food_pos[1]):
            self.snake.length += 1  # увеличиваем на 1 змейку, при поедании еды
            self.snake.score += 1


if __name__ == '__main__': # стартовая штука
    game = Game()
    print("Напишите номер модели, для открытия:")
    game.model_number = int(input())
    if not os.path.isdir("../Saves/" + str(game.model_number)):
        os.mkdir("../Saves/" + str(game.model_number))
        print("Модель не существует, было создано новое сохранение")
        logging.info(f"Было создано сохранение {str(game.model_number)}")
    else:
        game.neiro.read(game.model_number)
        print("Модель найдена, сохранение прочитано")
        logging.info(f"Открыто сохранение {str(game.model_number)}")
    game.run()
