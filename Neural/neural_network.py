import pygame
import random
import math
from App.const import *


class Neiro(object):
    def __init__(self):
        self.vhod = [0, 0, 0, 0, 0]
        self.vhod_to_vnutr = [[random.uniform(0, 1) for i in range(5)] for i in range(128)]
        self.vnutr1 = [0 for i in range(128)]
        self.vnutr_to_vnutr = [[random.uniform(0, 1) for i in range(128)] for i in range(128)]
        self.vnutr2 = [0 for i in range(128)]
        self.vnutr_to_vihod = [[random.uniform(0, 1) for i in range(128)] for i in range(4)]
        self.vihod = [0, 0, 0, 0]
        self.lirrate = 0.1

    def run(self, vhod):
        self.vhod = vhod
        self.vhod = self.vhod[-1]/1000 # делаем значение расстояния в float
        for i in range(128):  # считаем первый внутренний
            tmp_a = 0
            for j in range(5):
                tmp_a += self.sigmoid(self.vhod[j]) * self.vhod_to_vnutr[j][i]
            self.vnutr1[i] = tmp_a
        for i in range(128):  # считаем второй внутренний
            tmp_a = 0
            for j in range(128):
                tmp_a += self.sigmoid(self.vnutr1[j]) * self.vnutr_to_vnutr[j][i]
            self.vnutr2[i] = tmp_a
        for i in range(4):  # считаем выходной
            tmp_a = 0
            for j in range(128):
                tmp_a += self.sigmoid(self.vnutr2[j]) * self.vnutr_to_vihod[i][j]
            self.vihod[i] = tmp_a

        return self.vihod

    def learn(self, newdist, obst):
        pass

    def sigmoid(self, x):
         return 1 / (1 + math.exp(-x))

    def sigmoid_dx(self, x):
         sig = 1 / (1 + math.exp(-x))
         return sig * (1 - sig)
