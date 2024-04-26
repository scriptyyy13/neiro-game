import pygame
import random
from const import *


class Board(object):
    def __init__(self):
        self.size = BOARD_SIZE  # размер по горизонтали и вертикали соответственно
        self.s_size = SCREEN_SIZE # размер экрана, для отрисовки поля
        self.step = SNAKE_STEP  # размер сетки змейки

    def draw(self, screen):
        pygame.draw.rect(screen, (240, 240, 0),
                         pygame.Rect(0, 0, self.step, self.s_size[1]))
        pygame.draw.rect(screen, (240, 240, 0),
                         pygame.Rect(((self.s_size[0]-self.step) // self.step) * self.step, 0, self.step, self.s_size[1]))

        pygame.draw.rect(screen, (240, 240, 0),
                         pygame.Rect(0, 0, self.s_size[0], self.step))
        pygame.draw.rect(screen, (240, 240, 0),
                         pygame.Rect(0, ((self.s_size[1]-100)//self.step)*self.step, self.s_size[0], self.step))

    def get_wall_x(self): # получение стен по бокам (только x)
        return (0, ((self.s_size[0]-self.step) // self.step))

    def get_wall_y(self): # получение верхней и нижней стены (только y)
        return (0, ((self.s_size[1]-100)//self.step))