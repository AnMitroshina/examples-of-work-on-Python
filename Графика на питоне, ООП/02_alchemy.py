# -*- coding: utf-8 -*-
from termcolor import cprint, colored


class Water:
    def __add__(self, other):
        if isinstance(other, Air):
            return Storm()
        elif isinstance(other, Fire):
            return Steam()
        elif isinstance(other, Earth):
            return Dirt()
        elif isinstance(other, Water):
            return Bacteria()
        elif isinstance(other, Bacteria):
            return Plankton()
        elif isinstance(other, Grass):
            return Seaweed()

    def __str__(self):
        return 'Вода'


class Air:
    def __add__(self, other):
        if isinstance(other, Water):
            return Storm()
        elif isinstance(other, Fire):
            return Lightning()
        elif isinstance(other, Earth):
            return Dust()
        elif isinstance(other, Bacteria):
            return Bird()

    def __str__(self):
        return 'Воздух'


class Fire:
    def __add__(self, other):
        if isinstance(other, Water):
            return Steam()
        elif isinstance(other, Air):
            return Lightning()
        elif isinstance(other, Earth):
            return Lava()

    def __str__(self):
        return 'Огонь'


class Earth:
    def __add__(self, other):
        if isinstance(other, Water):
            return Dirt()
        elif isinstance(other, Air):
            return Dust()
        elif isinstance(other, Fire):
            return Lava()
        elif isinstance(other, Earth):
            return Grass()

    def __str__(self):
        return 'Земля'


class Bacteria:
    def __add__(self, other):
        if isinstance(other, Water):
            return Plankton()
        elif isinstance(other, Air):
            return Bird()

    def __str__(self):
        return 'Бактерия'


class Grass:
    def __add__(self, other):
        if isinstance(other, Water):
            return Seaweed()

    def __str__(self):
        return 'Трава'


class Storm:
    def __str__(self):
        return 'Шторм'


class Steam:
    def __str__(self):
        return 'Пар'


class Dirt:
    def __str__(self):
        return 'Грязь'


class Lightning:
    def __str__(self):
        return 'Молния'


class Lava:
    def __str__(self):
        return 'Лава'


class Dust:
    def __str__(self):
        return 'Пыль'


class Plankton:
    def __str__(self):
        return 'Планктон'


class Seaweed:
    def __str__(self):
        return 'Водоросли'


class Bird:
    def __str__(self):
        return 'Птица'


def print_elements(data):
    for i, key in enumerate(data):
        cprint('{} : {}'.format(i, key), color='grey')


def test_numbers(user_number, data):
    if user_number.isdigit():
        if len(user_number) == 1:
            user_number = int(user_number)
        else:
            cprint('Нужна всего одна цифра!)', color='red')
            return False
    else:
        cprint('Нужно число!', color='red')
        return False
    if user_number > len(data):
        cprint('Можно использовать только числа из спика!', color='red')
        return False
    else:
        return True


def get_element(index, data):
    for i, key in enumerate(data):
        if i == index:
            return data[key]


def test_minor_number(user_number):
    if user_number.isdigit():
        if len(user_number) == 1:
            user_number = int(user_number)
        else:
            cprint('Нужна всего одна цифра!)', color='red')
            return False
    else:
        cprint('Нужно число!', color='red')
        return False
    if user_number == 1 or user_number == 2:
        return user_number
    else:
        cprint('Нужно ввести 1 либо 2', color='red')
        return False


# def input_minor_number(data):
#     if data == new_elements:
#         while True:
#             show_new_elements = input('Для просмотра созданных элементов нажми 1, для продолжения нажми 2 :)')
#             test_res = test_minor_number(show_new_elements)
#             if test_res == 1:
#                 print('Ты создал:')
#                 print_elements(new_elements)
#                 break
#             elif test_res == 2:
#                 break
#
#     elif data == base_elements:
#         while True:
#             show_base_elements = input('Чтобы увидеть список базовых элементов, введи 1, или 2 для продолжения ')
#             test_res = test_minor_number(show_base_elements)
#             if test_res == 1:
#                 print('Ты можешь совместить:')
#                 print_elements(base_elements)
#             elif test_res == 2:
#                 break


base_elements = {
    'Вода': Water,
    'Воздух': Air,
    'Огонь': Fire,
    'Земля': Earth
}
new_elements = {}

cprint('Добро пожаловать в игру "Кто тут алхимик?"', color='green')
cprint('У тебя есть четыре элемента, попробуй совместить их попарно и посмотреть, что получится. '
       'Для магии введи номер элемента! ', color='green')

print_elements(base_elements)
while True:
    first_choice = input(colored('Выбери первый элемент: ', color='grey'))
    if test_numbers(first_choice, base_elements):
        user_number_1 = int(first_choice)
    else:
        continue
    second_choice = input(colored('Выбери второй элимент: ', color='grey'))
    if test_numbers(second_choice, base_elements):
        user_number_2 = int(second_choice)
    else:
        continue
    element_1 = get_element(user_number_1, base_elements)
    element_2 = get_element(user_number_2, base_elements)
    result = element_1() + element_2()
    if element_2 == element_1 and result is not None:
        if str(result) not in base_elements:
            base_elements[str(result)] = result.__class__
            cprint('Ого! Ты нашел еще один базовый элемент - {}! Попробуй сделать что-то с ним!'.format(result),
                   color='blue')
        else:
            cprint('У тебя уже есть такой элемент!', color='red')
    elif result is None:
        cprint('Элемент, который ты хочешь создать, невозможнен!', color='red')
    elif str(result) not in new_elements:
        cprint('И это.....{}!'.format(result), color='yellow')
        new_elements[str(result)] = result
    else:
        cprint('У тебя уже есть такой элемент!', color='red')

    if len(new_elements) >= 1:
        while True:
            show_new_elements = input(colored('Для просмотра созданных элементов нажми 1, для продолжения нажми 2 :) ',
                                              color='white'))
            test_res = test_minor_number(show_new_elements)
            if test_res == 1:
                cprint('Ты создал:', color='yellow')
                print_elements(new_elements)
                break
            elif test_res == 2:
                break
    while True:
        show_base_elements = input(colored('Чтобы увидеть список базовых элементов, введи 1, или 2 для продолжения ',
                                           color='white'))
        test_res = test_minor_number(show_base_elements)
        if test_res == 1:
            cprint('Ты можешь совместить:', color='yellow')
            print_elements(base_elements)
            break
        elif test_res == 2:
            break

# зачет!
