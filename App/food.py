import pygame
import random
from const import *


class Food(object):
    def __init__(self):
        self.time = FOOD_TIME_DIS  # время на исчезновение еды
        self.type = FOOD_TYPE  # типы еды (измененные спрайты)

    def spawn(self):  # спавн еды где-то на поле
        pass

    def disappear(self):  # исчезновение еды
        pass
