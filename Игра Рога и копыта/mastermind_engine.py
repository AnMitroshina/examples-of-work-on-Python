# -*- coding: utf-8 -*-
import simple_draw as sd
from random import choice

_holder = []


def make_number():
    global _holder
    _holder = []
    number_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(4):
        if i == 0:
            guessed_number = choice(number_list[1:])
            _holder.append(guessed_number)
            number_list.remove(guessed_number)
        else:
            guessed_number = choice(number_list)
            _holder.append(guessed_number)
            number_list.remove(guessed_number)
    return _holder


def check_number(user_number):
    _points = {'bulls': 0,
               'cows': 0}
    if len(user_number) == len(set(user_number)):
        for i in range(len(user_number)):
            if int(user_number[i]) == _holder[i]:
                _points['bulls'] += 1
            elif int(user_number[i]) in _holder:
                _points['cows'] += 1
        return _points
