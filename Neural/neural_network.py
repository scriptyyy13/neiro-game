import pygame
import random
import math
import numpy as np
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
        self.lirrate = 0.9
        self.prev_dist = 0
        self.prev_length = 0

    def run(self, vhod):
        self.vhod = vhod
        self.prev_dist = self.vhod[-1] # сохраняем прошлые значения для счета ошибки в конце итерации
        self.prev_length = self.vhod[-2]

        self.vhod[-1] = round(self.vhod[-1]/80, 7)  # делаем значение расстояние мелким значением
        self.vhod[-2] = round(self.vhod[-2]/3072, 7)   # делаем значение длинны змейки мелким значением

        for i in range(128):  # считаем первый внутренний
            tmp_a = 0
            for j in range(6):
                tmp_a += self.sigmoid(self.vhod[j]) * self.vhod_to_vnutr[i][j]
            tmp_a = round(tmp_a ,7)
            self.vnutr1[i] = tmp_a

        norm_n = max(self.vnutr1)+min(self.vnutr1)
        for i in range(128):  # нормализуем
            self.vnutr1[i] = self.vnutr1[i]/norm_n

        for i in range(128):  # считаем второй внутренний
            tmp_a = 0
            for j in range(128):
                tmp_a += self.sigmoid(self.vnutr1[j]) * self.vnutr_to_vnutr[j][i]
            tmp_a = round(tmp_a ,7)
            self.vnutr2[i] = tmp_a

            norm_n = max(self.vnutr2) + min(self.vnutr2)
            for i in range(128):  # нормализуем
                self.vnutr2[i] = self.vnutr2[i] / norm_n

        for i in range(4):  # считаем выходной
            tmp_a = 0
            for j in range(128):
                tmp_a += self.sigmoid(self.vnutr2[j]) * self.vnutr_to_vihod[i][j]
            tmp_a = round(tmp_a ,7)
            self.vihod[i] = round(self.sigmoid(tmp_a), 7)

        #norm_n = max(self.vihod) + min(self.vihod)
        #for i in range(4):  # нормализуем
        #    self.vihod[i] = self.vihod[i] / norm_n

        return self.vihod

    def learn(self, new_dist, new_length):
        best = 0
        best_index = 0
        for i in range(4):
            if (self.vihod[i] > best):
                best = self.vihod[i]
                best_index = i
            if (new_length < self.prev_length):
                error_best = best
            elif (new_dist >= self.prev_dist):
                error_best = best
            else:
                error_best = 1 - best
        print('err: ', error_best, self.vihod)
        for idx in range(4): # идем от каждого выходного значения
            if (best_index == idx):
                error = error_best
            else:
                error = self.vhod[idx]
            print("!!! err: ", idx, error)
            wdelta = error * self.sigmoid(self.vihod[idx])
            for j in range(128):
                self.vnutr_to_vihod[idx][j] = self.vnutr_to_vihod[idx][j] - self.vnutr2[j] * wdelta * self.lirrate
            for i in range(128):
                error_lvl_one = wdelta * self.vnutr_to_vnutr[i][idx]
                wdelta_lvl_one = error_lvl_one * self.sigmoid(self.vnutr1[idx])
                for j in range(128):
                    self.vnutr_to_vnutr[i][j] = self.vnutr_to_vnutr[i][j] - self.vnutr1[j] * wdelta_lvl_one * self.lirrate

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_dx(self, x):
         sig = 1 / (1 + np.exp(-x))
         return sig * (1 - sig)
