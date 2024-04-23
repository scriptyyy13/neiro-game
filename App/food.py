import pygame
import random
from const import *


class Food(object):
    def __init__(self):
        self.time = FOOD_TIME_DIS  # время на исчезновение еды
        self.type = FOOD_TYPE  # типы еды (измененные спрайты)
        self.step = SNAKE_STEP  # размер сетки
        self.food_pos = (2, 1)  # позиция еды

    def draw(self, screen):  # отрисовка еды
        pygame.draw.rect(screen, (0, 240, 0),
                         pygame.Rect(self.food_pos[0] * self.step, self.food_pos[1] * self.step, self.step, self.step))

    def update(self, pos):  # спавн еды где-то на поле и деспавн при поедании
        posx = self.food_pos[0]
        posy = self.food_pos[1]
        while [posx, posy] in pos:
            posx = random.randint(1, BOARD_SIZE[0] // self.step)
            posy = random.randint(1, BOARD_SIZE[1] // self.step)
            self.food_pos = (posx, posy)
