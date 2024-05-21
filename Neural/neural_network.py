import pygame
import random
import math
from App.const import *


class Neiro(object):
    def __init__(self):
        self.vhod = [0, 0, 0, 0, 0, 0] # первые четыре это значения наличия препятствия, пятое длинна змейки, шестое - расстояние до еды
        self.vhod_to_vnutr = [[random.uniform(0, 1) for i in range(6)] for i in range(128)]
        self.vnutr1 = [0 for i in range(128)]
        self.vnutr_to_vnutr = [[random.uniform(0, 1) for i in range(128)] for i in range(128)]
        self.vnutr2 = [0 for i in range(128)]
        self.vnutr_to_vihod = [[random.uniform(0, 1) for i in range(128)] for i in range(4)]
        self.vihod = [0, 0, 0, 0]
        self.lirrate = 0.1
        self.prev_dist = 0
        self.prev_length = 0

    def run(self, vhod):
        self.vhod = vhod
        self.prev_dist = self.vhod[-1] # сохраняем прошлые значения для счета ошибки в конце итерации
        self.prev_length = self.vhod[-2]

        self.vhod[-1] = self.sigmoid(self.vhod[-1])  # делаем значение расстояние мелким значением
        self.vhod[-2] = self.sigmoid(self.vhod[-2])  # делаем значение длинны змейки мелким значением
        for i in range(128):  # считаем первый внутренний
            tmp_a = 0
            for j in range(6):
                tmp_a += self.sigmoid(self.vhod[j]) * self.vhod_to_vnutr[i][j]
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
            self.vihod[i] = self.sigmoid(tmp_a)
        return self.vihod

    def learn(self, new_dist, new_length):
        best = 0
        best_index = 0
        for i in range(4):
            if (self.vihod[i]>best):
                best = self.vihod[i]
                best_index = i
        if (new_length < self.prev_length):
            error = best
        elif (new_dist >= self.prev_dist):
            error = best
        else:
            error = 1 - best
        wdelta = error * self.sigmoid(self.vihod[best_index])
        for j in range(128):
            self.vnutr_to_vihod[best_index][j] = self.vnutr_to_vihod[best_index][j] - self.vnutr2[j] * wdelta * self.lirrate
        for i in range(128):
            for j in range(128):
                wdelta = error * self.sigmoid(self.vnutr1[j])
                self.vnutr_to_vnutr[i][j] = self.vnutr_to_vnutr[i][j] - self.vnutr1[j] * wdelta * self.lirrate
        for i in range(128):
            for j in range(6):
                wdelta = error * self.sigmoid(self.vhod[j])
                self.vhod_to_vnutr[i][j] = self.vhod_to_vnutr[i][j] - self.vhod[j] * wdelta * self.lirrate

    def sigmoid(self, x):
         return 1 / (1 + math.exp(-x))

    def sigmoid_dx(self, x):
         sig = 1 / (1 + math.exp(-x))
         return sig * (1 - sig)
