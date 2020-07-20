# -*- coding: utf-8 -*-

import simple_draw as sd
from snowfall import create_snowflakes, draw_color_snowflakes, move_snowflakes, del_snowflakes, get_fallen_snowflakes

# На основе кода из lesson_004/05_snowfall.py
# сделать модуль snowfall.py в котором реализовать следующие функции
#  создать_снежинки(N) - создает N снежинок
#  нарисовать_снежинки_цветом(color) - отрисовывает все снежинки цветом color
#  сдвинуть_снежинки() - сдвигает снежинки на один шаг
#  номера_достигших_низа_экрана() - выдает список номеров снежинок, которые вышли за границу экрана
#  удалить_снежинки(номера) - удаляет снежинки с номерами из списка
#
# В текущем модуле реализовать главный цикл падения снежинок,
# обращаясь ТОЛЬКО к функциям модуля snowfall

create_snowflakes(30)
while True:
    draw_color_snowflakes()
    move_snowflakes()
    draw_color_snowflakes(color=sd.random_color())
    list_fallen_snowflakes = get_fallen_snowflakes()
    if list_fallen_snowflakes:
        count = del_snowflakes(list_fallen_snowflakes)
        create_snowflakes(count)
    sd.sleep(0.01)
    if sd.user_want_exit():
        break

sd.pause()

# зачет!
