# -*- coding: utf-8 -*-
from random import randint

import simple_draw as sd


# Шаг 1: Реализовать падение снежинки через класс. Внести в методы:
#  - создание снежинки с нужными параметрами
#  - отработку изменений координат
#  - отрисовку


class Snowflake:
    def __init__(self):
        self.x = randint(50, sd.resolution[0])
        self.y = randint(sd.resolution[1], sd.resolution[1] * 1.5)
        self.length = randint(10, 80)

    def __str__(self):
        return 'Snowflake: x = {}, y = {}, length = {}'.format(self.x, self.y, self.length)

    def clear_previous_picture(self):
        point = sd.get_point(self.x, self.y)
        sd.snowflake(center=point, length=self.length, color=sd.background_color)

    def move(self):
        self.x += randint(-10, 10)
        self.y -= randint(10, 20)

    def draw(self):
        point = sd.get_point(self.x, self.y)
        sd.snowflake(center=point, length=self.length, color=sd.COLOR_WHITE)

    def can_fall(self):
        return self.y < -self.length


flake = Snowflake()


# print(str(flake))
# while True:
#     flake.clear_previous_picture()
#     flake.move()
#     flake.draw()
#     if flake.can_fall():
#         break
#     sd.sleep(0.1)
#     if sd.user_want_exit():
#         break


def get_flakes(count=2):  # Эта функция была уже готовой на прошлой проверке, её не нужно дорабатывать
    #  мне тогда не понятно, почему так? Разве мы не ставим сейчас в зависимость от окружения эту функцию?
    # TODO Нет конечно. Если вас смутило одинаковое имя flakes, то на это есть области видимости, внутри функции своя
    #  область видимости и чтобы flakes была общей с внешней областью видимости её нужно отдельно объявить, что она
    #  "внешняя" переменная: global flakes. Легко можно поменять имя и убедиться что ничего не изменилось:
    additional_flakes = []
    for i in range(count):
        flake_0 = Snowflake()
        additional_flakes.append(flake_0)
    return additional_flakes

# восстановил на всякий случай
# def get_flakes(count=2):
#     new_flakes = []
#     for i in range(count):
#         new_flakes.append(Snowflake())
#     return new_flakes


def get_fallen_flakes(data):
    #  Чтобы функция была чистой, нужно получать данные через аргументы, поэтому передайте список снежинок flakes
    #  через аргумент фукнции
    #  я верно понимаю, что это необходимо для того, чтобы она была "независима" от параметров,
    #   чтобы она работала при любых других вводных?
    #  идеально, когда функция зависит только от своих аргументов, и совсем не зависит от окружения. Такая функция
    #  всегда выдаёт один и тот же результат, её легко тестировать и дорабатывать. Почитайте про "чистые функции" - это
    #  важная базовая концепция.
    # Прочитала, но не стало от этого понятнее с функцией выше.
    print(flakes)
    for element in data:
        if element.can_fall():
            data.remove(element)
            print("data", data)
        return data


# шаг 2: создать снегопад - список объектов Снежинка в отдельном списке, обработку примерно так:
flakes = get_flakes(count=30)

while True:
    sd.start_drawing()
    quantity = 0
    for flake in flakes:
        flake.clear_previous_picture()
        flake.move()
        flake.draw()
    for flake in flakes:  # если делать во время первого цикла фор, снежинки "тормозятся" из-за удаления снежинки,
        # поэтому вынесла
        if flake.can_fall():
            flakes.remove(flake)
            quantity += 1

    new_flakes = get_flakes(count=quantity)  # добавить еще сверху
    # тут надо было к списку flakes с помощью extend() добавить список новых снежинок полученных от get_flakes
    # настолько очевидно, что стыдно :(
    flakes.extend(new_flakes)
    sd.finish_drawing()
    sd.sleep(0.1)
    if sd.user_want_exit():
        break

sd.pause()

# зачет!
