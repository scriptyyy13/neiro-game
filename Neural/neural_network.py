import pygame
import random
import math
import os
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
        self.lirrate = 0.4
        self.prev_dist = 0
        self.prev_length = 0

    def save(self, number): # сохранить
        matrix = self.vhod_to_vnutr
        if not os.path.isdir("../Saves/" + str(number)):
            os.mkdir("../Saves/" + str(number))
        with open("../Saves/" + str(number)+"/vhod_to_vnutr_" + str(number) + ".txt", "w") as f:
            f.write('\n'.join([' '.join(map(str, line)) for line in matrix]))

        matrix = self.vnutr_to_vnutr
        with open("../Saves/" + str(number)+"/vnutr_to_vnutr_" + str(number) + ".txt", "w") as f:
            f.write('\n'.join([' '.join(map(str, line)) for line in matrix]))

        matrix = self.vnutr_to_vihod
        with open("../Saves/" + str(number)+"/vnutr_to_vihod_" + str(number) + ".txt", "w") as f:
            f.write('\n'.join([' '.join(map(str, line)) for line in matrix]))

    def read(self, number): # последнее сохранение
        f = open("../Saves/" + str(number)+"/vhod_to_vnutr_" + str(number) + ".txt")
        to_save = []
        for line in f:
            to_save.append(list(map(float, line.replace("\n", '').split())))
        self.vhod_to_vnutr = to_save

        f = open("../Saves/" + str(number)+"/vnutr_to_vnutr_" + str(number) + ".txt")
        to_save = []
        for line in f:
            to_save.append(list(map(float, line.replace("\n", '').split())))
        self.vnutr_to_vnutr = to_save

        f = open("../Saves/" + str(number)+"/vnutr_to_vihod_" + str(number) + ".txt")
        to_save = []
        for line in f:
            to_save.append(list(map(float, line.replace("\n", '').split())))
        self.vnutr_to_vihod = to_save


    def run(self, vhod):
        self.vhod = vhod
        self.prev_dist = self.vhod[-1] # сохраняем прошлые значения для счета ошибки в конце итерации
        self.prev_length = self.vhod[-2]

        self.vhod[-1] = round(self.vhod[-1]/80, 7)  # делаем значение расстояние мелким значением
        self.vhod[-2] = round(self.vhod[-2]/3072, 7)   # делаем значение длинны змейки мелким значением

        for i in range(128):  # считаем первый внутренний
            tmp_a = 0
            for j in range(6):
                tmp_a += self.vhod[j] * self.vhod_to_vnutr[i][j]
            tmp_a = round(tmp_a, 7)
            self.vnutr1[i] = tmp_a

        norm_n = max(self.vnutr1)+min(self.vnutr1)
        for i in range(128):  # нормализуем
            self.vnutr1[i] = round(self.vnutr1[i]/norm_n, 7)

        for i in range(128):  # считаем второй внутренний
            tmp_a = 0
            for j in range(128):
                tmp_a += self.vnutr1[j] * self.vnutr_to_vnutr[j][i]
            tmp_a = round(tmp_a, 7)
            self.vnutr2[i] = tmp_a

        tmp_mm = min(self.vnutr2)
        if (tmp_mm < 0):
            tmp_mm*=-1

        norm_n = max(self.vnutr2) + tmp_mm
        for i in range(128):  # нормализуем
            self.vnutr2[i] = round(self.vnutr2[i] / norm_n, 7)

        for i in range(4):  # считаем выходной
            tmp_a = 0
            for j in range(128):
                tmp_a += self.vnutr2[j] * self.vnutr_to_vihod[i][j]
            tmp_a = round(tmp_a, 7)
            self.vihod[i] = round(tmp_a, 7)

        tmp_mm = min(self.vihod)
        if (tmp_mm < 0):
            tmp_mm *= -1

        norm_n = max(self.vihod) + tmp_mm
        for i in range(4):  # нормализуем
            self.vihod[i] = round(self.vihod[i] / norm_n, 7)
        return self.vihod

    def learn(self, new_dist, new_length, snake, foodcoords, nearobs):
        sled_steps = [0, 0, 0, 0]
        now_snake = snake[-1]
        for i in range(4):
            if (i == 0):
                tmp_new_snake = (now_snake[0] + 1, now_snake[1])
            if (i == 1):
                tmp_new_snake = (now_snake[0] - 1, now_snake[1])
            if (i == 2):
                tmp_new_snake = (now_snake[0], now_snake[1] + 1)
            if (i == 3):
                tmp_new_snake = (now_snake[0], now_snake[1] - 1)
            new_dist_food = round(math.hypot(foodcoords[0] - tmp_new_snake[0], foodcoords[1] - tmp_new_snake[1]), 3)
            if (new_dist_food < new_dist and nearobs[i]==False):
                sled_steps[i] = 1

        for idx in range(4): # идем от каждого выходного значения
            error = abs(sled_steps[idx]-self.vhod[idx])
            wdelta = error * self.vihod[idx]

            mini = float('+INF')
            maxi = float('-INF')
            for j in range(128):
                self.vnutr_to_vihod[idx][j] = self.vnutr_to_vihod[idx][j] - self.vnutr2[j] * wdelta * self.lirrate
                if (mini > self.vnutr_to_vihod[idx][j]):
                    mini = self.vnutr_to_vihod[idx][j]
                if (maxi < self.vnutr_to_vihod[idx][j]):
                    maxi = self.vnutr_to_vihod[idx][j]
            for j in range(128):
                self.vnutr_to_vihod[idx][j] += abs(mini)
            for j in range(128):
                self.vnutr_to_vihod[idx][j]=self.vnutr_to_vihod[idx][j]/(maxi+abs(mini))

            for i in range(128):
                error_lvl_one = wdelta * self.vnutr_to_vnutr[i][idx]
                wdelta_lvl_one = error_lvl_one * self.vnutr1[idx]
                mini = float('+INF')
                maxi = float('-INF')
                for j in range(128):
                    self.vnutr_to_vnutr[i][j] = self.vnutr_to_vnutr[i][j] - self.vnutr1[j] * wdelta_lvl_one * self.lirrate
                    if (mini > self.vnutr_to_vnutr[i][j]):
                        mini = self.vnutr_to_vnutr[i][j]
                    if (maxi < self.vnutr_to_vnutr[i][j]):
                        maxi = self.vnutr_to_vnutr[i][j]
                for j in range(128):
                    self.vnutr_to_vnutr[i][j] += abs(mini)
                for j in range(128):
                    self.vnutr_to_vnutr[i][j] = self.vnutr_to_vnutr[i][j] / (maxi + abs(mini))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_dx(self, x):
         sig = 1 / (1 + np.exp(-x))
         return sig * (1 - sig)
