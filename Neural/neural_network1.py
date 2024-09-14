import pygame
import random
import math
import os
import numpy as np
from App.const import *


class Neiro(object):
    """ В классе Neiro происходят все действия с нейронкой

    save сохроняет нейронку в папку с номером

    read считывает сохронение нейронки с определенным номером

    count_vnutr1 подсчитывает первый внутренний слой

    count_vnutr2 подсчитывает второй внутренний слой

    count_vihod подсчитывает выходной слой

    run основной метод работы нейронки, задействует подсчеты слоев

    learn метод обучения

    count_error подсчитать ошибку

    count_learn обучается, учитывая ошибку

    """
    def __init__(self):
        self.vhod = np.zeros(
            6)  # первые четыре это значения наличия препятствия, пятое длинна змейки, шестое - расстояние до еды
        self.vhod_to_vnutr = np.random.uniform(0, 1, (128, 6))
        self.vnutr1 = np.zeros(128)
        self.vnutr_to_vnutr = np.random.uniform(0, 1, (128, 128))
        self.vnutr2 = np.zeros(128)
        self.vnutr_to_vihod = np.random.uniform(0, 1, (128, 4))
        self.vihod = np.zeros(4)
        self.lirrate = 0.9 # скорость обучения

    def save(self, number):  # сохранение
        matrix = self.vhod_to_vnutr
        if not os.path.isdir("../Saves/" + str(number)):
            os.mkdir("../Saves/" + str(number))
        with open("../Saves/" + str(number) + "/vhod_to_vnutr_" + str(number) + ".txt", "w") as f:
            f.write('\n'.join([' '.join(map(str, line)) for line in matrix])) # сохранение из входного в внутренний

        matrix = self.vnutr_to_vnutr
        with open("../Saves/" + str(number) + "/vnutr_to_vnutr_" + str(number) + ".txt", "w") as f:
            f.write('\n'.join([' '.join(map(str, line)) for line in matrix])) # сохранение из внутреннего в второй внутренний

        matrix = self.vnutr_to_vihod
        with open("../Saves/" + str(number) + "/vnutr_to_vihod_" + str(number) + ".txt", "w") as f:
            f.write('\n'.join([' '.join(map(str, line)) for line in matrix])) # сохранение из второго втурненнего во выходной

    def read(self, number):  # чтение сохранения
        f = open("../Saves/" + str(number) + "/vhod_to_vnutr_" + str(number) + ".txt")
        to_save = []
        for line in f: # из входного во внутренний
            to_save.append(list(map(float, line.replace("\n", '').split())))
        self.vhod_to_vnutr = np.array(to_save)

        f = open("../Saves/" + str(number) + "/vnutr_to_vnutr_" + str(number) + ".txt")
        to_save = []
        for line in f: # из внутреннего во второй внутренний
            to_save.append(list(map(float, line.replace("\n", '').split())))
        self.vnutr_to_vnutr = np.array(to_save)

        f = open("../Saves/" + str(number) + "/vnutr_to_vihod_" + str(number) + ".txt")
        to_save = []
        for line in f: # из второго внутреннего в выходной
            to_save.append(list(map(float, line.replace("\n", '').split())))
        self.vnutr_to_vihod = np.array(to_save)

    def count_vnutr1(self): # подсчет из первого внутреннего
        self.vnutr1 = np.round(np.dot(self.vhod_to_vnutr, self.vhod), 7)
        norm_n = max(self.vnutr1) + min(self.vnutr1)
        for i in range(128):  # нормализуем
            self.vnutr1[i] = round(self.vnutr1[i] / norm_n, 7)

    def count_vnutr2(self): # подсчет второго внутреннего
        self.vnutr2 = np.round(np.dot(self.vnutr1, self.vnutr_to_vnutr), 7)
        tmp_mm = min(self.vnutr2)
        if (tmp_mm < 0):
            tmp_mm *= -1
        norm_n = max(self.vnutr2) + tmp_mm
        for i in range(128):  # нормализуем
            self.vnutr2[i] = round(self.vnutr2[i] / norm_n, 7)

    def count_vihod(self): # подсчет выходного слоя
        self.vihod = np.round(np.dot(self.vnutr_to_vihod, self.vnutr2), 7)
        tmp_mm = min(self.vihod)
        if (tmp_mm < 0):
            tmp_mm *= -1
        norm_n = max(self.vihod) + tmp_mm
        for i in range(4):  # нормализуем
            self.vihod[i] = round(self.vihod[i] / norm_n, 7)

    def run(self, vhod):
        self.vhod = vhod
        self.vhod[-1] = round(self.vhod[-1] / 80, 7)  # делаем значение расстояние мелким значением
        self.vhod[-2] = round(self.vhod[-2] / 3072, 7)  # делаем значение длинны змейки мелким значением

        self.count_vnutr1()
        self.count_vnutr2()
        self.count_vihod()

        return self.vihod

    def count_error(self, sled_steps, now_snake, foodcoords, nearobs, new_dist): # подсчет ошибки
        for i in range(4): # вычисляем лучший ход
            if (i == 0):
                tmp_new_snake = (now_snake[0] + 1, now_snake[1])
            if (i == 1):
                tmp_new_snake = (now_snake[0] - 1, now_snake[1])
            if (i == 2):
                tmp_new_snake = (now_snake[0], now_snake[1] + 1)
            if (i == 3):
                tmp_new_snake = (now_snake[0], now_snake[1] - 1)
            new_dist_food = round(math.hypot(foodcoords[0] - tmp_new_snake[0], foodcoords[1] - tmp_new_snake[1]), 3)
            if (new_dist_food < new_dist and nearobs[i] == False):
                sled_steps[i] = 1
        return sled_steps # получаем ошибку

    def count_learn(self, sled_steps):
        for idx in range(4):  # идем от каждого выходного значения
            error = abs(sled_steps[idx] - self.vhod[idx])
            wdelta = error * self.vihod[idx]
            mini = float('+INF')
            maxi = float('-INF')
            for j in range(128):
                self.vnutr_to_vihod[idx][j] = self.vnutr_to_vihod[idx][j] - self.vnutr2[j] * wdelta * self.lirrate # вычисляем новые значения весов
                if (mini > self.vnutr_to_vihod[idx][j]):
                    mini = self.vnutr_to_vihod[idx][j]
                if (maxi < self.vnutr_to_vihod[idx][j]):
                    maxi = self.vnutr_to_vihod[idx][j]
            for j in range(128):
                self.vnutr_to_vihod[idx][j] += abs(mini)
            for j in range(128):
                self.vnutr_to_vihod[idx][j] = self.vnutr_to_vihod[idx][j] / (maxi + abs(mini))   # нормализуем

            error_lvl_one = wdelta * self.vnutr_to_vnutr[:, idx]
            wdelta_lvl_one = error_lvl_one * self.vnutr1[idx]

            self.vnutr_to_vnutr -= (self.vnutr1[:, np.newaxis] * wdelta_lvl_one) * self.lirrate # вычисляем новые значения весов

            mini = np.min(self.vnutr_to_vnutr, axis=1)
            maxi = np.max(self.vnutr_to_vnutr, axis=1)

            self.vnutr_to_vnutr += np.abs(mini)[:, np.newaxis]  # нормализуем
            self.vnutr_to_vnutr /= (maxi + np.abs(mini))[:, np.newaxis] # нормализуем

    def learn(self, new_dist, new_length, snake, foodcoords, nearobs): # обучаем
        sled_steps = [0, 0, 0, 0]
        now_snake = snake[-1]
        sled_steps = self.count_error(sled_steps, now_snake, foodcoords, nearobs, new_dist)
        self.count_learn(sled_steps)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_dx(self, x):
        sig = 1 / (1 + np.exp(-x))
        return sig * (1 - sig)
