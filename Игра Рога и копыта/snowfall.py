# -*- coding: utf-8 -*-
import simple_draw as sd

x_list = []
y_list = []
lengths_list = []
fallen_snowflakes = []


def create_snowflakes(n=20):
    for i in range(n):
        x = sd.random_number(50, sd.resolution[0])
        x_list.append(x)
        y = sd.random_number(sd.resolution[1], sd.resolution[1] * 2)
        y_list.append(y)
        length = sd.random_number(10, 50)
        lengths_list.append(length)


def draw_color_snowflakes(color=sd.background_color):
    for index, length in enumerate(lengths_list):
        x = x_list[index]
        y = y_list[index]
        point = sd.get_point(x=x, y=y)
        sd.snowflake(center=point, length=length, color=color)


def move_snowflakes():
    for i in range(len(x_list)):
        x_list[i] += sd.random_number(-10, 10)
        y_list[i] -= sd.random_number(10, 20)


def get_fallen_snowflakes():
    global fallen_snowflakes
    fallen_snowflakes = []
    for index, y in enumerate(y_list):
        if y < -lengths_list[index]:  # не нравится мне сравнивать с длиной, снежинки в этом случе начинают застревать
            # https://prnt.sc/r1fgbe. Тогда их нужно дополнительно
            # Это называется сугроб и это некоторым нравится :) Ок, просто сделал отрицательным и этого как раз
            #  хватит
            # Да я уже додумалась до этого после отправки... Спасибо!
            fallen_snowflakes.append(index)
    return fallen_snowflakes


def del_snowflakes(data):
    count = len(data)
    for index, del_index in enumerate(sorted(data, reverse=True)):
        del y_list[del_index]
        del x_list[del_index]
        del lengths_list[del_index]
    return count
