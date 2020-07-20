# -*- coding: utf-8 -*-

# Игра «Быки и коровы»
# https://goo.gl/Go2mb9
#
# Правила:
# Компьютер загадывает четырехзначное число, все цифры которого различны
# (первая цифра числа отлична от нуля). Игроку необходимо разгадать задуманное число.
# Игрок вводит четырехзначное число c неповторяющимися цифрами,
# компьютер сообщают о количестве «быков» и «коров» в названном числе
# «бык» — цифра есть в записи задуманного числа и стоит в той же позиции,
#       что и в задуманном числе
# «корова» — цифра есть в записи задуманного числа, но не стоит в той же позиции,
#       что и в задуманном числе
#
# Например, если задумано число 3275 и названо число 1234,
# получаем в названном числе одного «быка» и одну «корову».
# Очевидно, что число отгадано в том случае, если имеем 4 «быка».
#
# Формат ответа компьютера
# > быки - 1, коровы - 1


# Составить отдельный модуль mastermind_engine, реализующий функциональность игры.
# В этом модуле нужно реализовать функции:
#   загадать_число()
#   проверить_число(NN) - возвращает словарь {'bulls': N, 'cows': N}
# Загаданное число хранить в глобальной переменной.
# Обратите внимание, что строки - это список символов.
#
# В текущем модуле (lesson_006/01_mastermind.py) реализовать логику работы с пользователем:
#   модуль движка загадывает число
#   в цикле, пока число не отгадано
#       у пользователя запрашивается вариант числа
#       модуль движка проверяет число и выдает быков/коров
#       результат быков/коров выводится на консоль
#  когда игрок угадал таки число - показать количество ходов и вопрос "Хотите еще партию?"
#
# При написании кода учитывайте, что движок игры никак не должен взаимодействовать с пользователем.
# Все общение с пользователем делать в текущем модуле. Представьте, что движок игры могут использовать
# разные клиенты - веб, чатбот, приложение, етс - они знают как спрашивать и отвечать пользователю.
# Движок игры реализует только саму функциональность игры.
# Это пример применения SOLID принципа (см https://goo.gl/GFMoaI) в архитектуре программ.
# Точнее, в этом случае важен принцип единственной ответственности - https://goo.gl/rYb3hT
from random import choice

from lesson_006.mastermind_engine import make_number, check_number
from termcolor import cprint, colored

dict_phrases = {'bulls': ['Быки атакуют!', 'Бычок селен', 'Кажется быки сейчас победят', 'Бык быка видит из далека',
                          'Чем меньше мозг, тем длиньше рог', 'Бычество - не порок'],
                'cows': ['Муууу', 'Коровку, ннадо?', '"Слово – не воробей", а корова! Накроет лепёшкой – не отмоешься',
                         'Упрямо отказывая в молоке, корова всё равно быком не станет',
                         'Корова бадается', 'Коровы ведут'],
                'draw': ['Что-то интересненькое', 'Напряженная борьба', 'Делаю ставки на быка!',
                         'Жареньким запахло, интересно, Коровой или Быком']}


# Отличное разнообразие в игре!
# спасибо!


def set_game(number_attempts):
    while True:
        print('Твоя попытка номер', number_attempts)
        user_number = input(colored('Введи число:', color='green'))
        if user_number.isdigit():
            user_number = list(user_number)
        else:
            cprint('Число должно состоять из цифр!', color='red')
            continue
        if test_numbers(user_number):
            result = check_number(user_number)
            if result['bulls'] == 4:
                number_attempts += 1
                cprint('Количество игр {}'.format(number_attempts), color='yellow')
                restart = input(colored('Для продолжения введи 1, для выхода 0:)', color='yellow'))
                if restart == '1':
                    cprint('Вперед!', color='green')
                    cprint('Число загадано!', color='green')
                    number_attempts = 0
                    make_number()
                else:
                    cprint('Будем скучать :(', color='grey')
                    break

            else:
                number_attempts += 1
                cprint('Твой результат:', color='cyan')
                cprint('Быки: {}, Коровы: {}'.format(result['bulls'], result['cows']), color='blue', attrs=['reverse'])
                if result['bulls'] > result['cows']:
                    cprint('{}'.format(choice(dict_phrases['bulls'])), color='blue')
                elif result['bulls'] < result['cows']:
                    cprint('{}'.format(choice(dict_phrases['cows'])), color='blue')
                elif result['bulls'] == result['cows']:
                    cprint('{}'.format(choice(dict_phrases['draw'])), color='blue')


def test_numbers(user_number):
    for i in range(len(user_number)):
        user_number[i] = int(user_number[i])
        if i == 0 and user_number[i] == 0:
            cprint('Первое число не может быть 0!', color='red')
            return False
    if len(user_number) != len(set(user_number)):
        cprint('Цифры в числе должны быть уникальными!', color='red')
        return False
    elif len(user_number) != 4:
        cprint('Число должно содержать четыре цифры!', color='red')
        return False
    return user_number


cprint('Добро пожаловать в игру "Быки и Коровы"!', color='yellow')
make_number()
cprint('Мы загадали 4-ех значное число, попробуй угадать!', color='green')
while True:
    answer = int(input('Для старта нажми 1, для выхода 0?'))
    if answer == 1:
        set_game(number_attempts=0)
        break
    else:
        cprint('Будем тебя ждать!', color='grey')
        break

# зачет!
