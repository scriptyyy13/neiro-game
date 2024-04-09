import pygame
import random


class Food(object):
    def __init__(self):
        self.time = 40  # время на исчезновение еды
        self.type = 1  # типы еды (измененные спрайты)

    def spawn(self): # спавн еды где-то на поле
        pass

    def disappear(self): # исчезновение еды
        pass