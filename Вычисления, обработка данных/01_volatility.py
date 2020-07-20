# -*- coding: utf-8 -*-


# Описание предметной области:
#
# При торгах на бирже совершаются сделки - один купил, второй продал.
# Покупают и продают ценные бумаги (акции, облигации, фьючерсы, етс). Ценные бумаги - это по сути долговые расписки.
# Ценные бумаги выпускаются партиями, от десятка до несколько миллионов штук.
# Каждая такая партия (выпуск) имеет свой торговый код на бирже - тикер - https://goo.gl/MJQ5Lq
# Все бумаги из этой партии (выпуска) одинаковы в цене, поэтому говорят о цене одной бумаги.
# У разных выпусков бумаг - разные цены, которые могут отличаться в сотни и тысячи раз.
# Каждая биржевая сделка характеризуется:
#   тикер ценнной бумаги
#   время сделки
#   цена сделки
#   обьем сделки (сколько ценных бумаг было куплено)
#
# В ходе торгов цены сделок могут со временем расти и понижаться. Величина изменения цен называтея волатильностью.
# Например, если бумага №1 торговалась с ценами 11, 11, 12, 11, 12, 11, 11, 11 - то она мало волатильна.
# А если у бумаги №2 цены сделок были: 20, 15, 23, 56, 100, 50, 3, 10 - то такая бумага имеет большую волатильность.
# Волатильность можно считать разными способами, мы будем считать сильно упрощенным способом -
# отклонение в процентах от средней цены за торговую сессию:
#   средняя цена = (максимальная цена + минимальная цена) / 2
#   волатильность = ((максимальная цена - минимальная цена) / средняя цена) * 100%
# Например для бумаги №1:
#   average_price = (12 + 11) / 2 = 11.5
#   volatility = ((12 - 11) / average_price) * 100 = 8.7%
# Для бумаги №2:
#   average_price = (100 + 3) / 2 = 51.5
#   volatility = ((100 - 3) / average_price) * 100 = 188.34%
#
# В реальности волатильность рассчитывается так: https://goo.gl/VJNmmY
#
# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью.
# Бумаги с нулевой волатильностью вывести отдельно.
# Результаты вывести на консоль в виде:
#   Максимальная волатильность:
#       ТИКЕР1 - ХХХ.ХХ %
#       ТИКЕР2 - ХХХ.ХХ %
#       ТИКЕР3 - ХХХ.ХХ %
#   Минимальная волатильность:
#       ТИКЕР4 - ХХХ.ХХ %
#       ТИКЕР5 - ХХХ.ХХ %
#       ТИКЕР6 - ХХХ.ХХ %
#   Нулевая волатильность:
#       ТИКЕР7, ТИКЕР8, ТИКЕР9, ТИКЕР10, ТИКЕР11, ТИКЕР12
# Волатильности указывать в порядке убывания. Тикеры с нулевой волатильностью упорядочить по имени.
#
# Подготовка исходных данных
# 1. Скачать файл https://drive.google.com/file/d/1l5sia-9c-t91iIPiGyBc1s9mQ8RgTNqb/view?usp=sharing
#       (обратите внимание на значок скачивания в правом верхнем углу,
#       см https://drive.google.com/file/d/1M6mW1jI2RdZhdSCEmlbFi5eoAXOR3u6G/view?usp=sharing)
# 2. Раззиповать средствами операционной системы содержимое архива
#       в папку python_base_source/lesson_012/trades
# 3. В каждом файле в папке trades содержится данные по сделакам по одному тикеру, разделенные запятыми.
#   Первая строка - название колонок:
#       SECID - тикер
#       TRADETIME - время сделки
#       PRICE - цена сделки
#       QUANTITY - количество бумаг в этой сделке
#   Все последующие строки в файле - данные о сделках
#
# Подсказка: нужно последовательно открывать каждый файл, вычитывать данные, высчитывать волатильность и запоминать.
# Вывод на консоль можно сделать только после обработки всех файлов.
#
# Для плавного перехода к мультипоточности, код оформить в обьектном стиле, используя следующий каркас
#
# class <Название класса>:
#
#     def __init__(self, <параметры>):
#         <сохранение параметров>
#
#     def run(self):
#         <обработка данных>
########################################################################################################################
import os
from collections import defaultdict

FILE_NAME = 'trades'


class CalcVolatility:

    def __init__(self, file_name):
        self.file_name = file_name
        self.prices = defaultdict(list)


    def run(self):
        self.get_prices()
        self.get_volatilities()


    def get_prices(self):
        # Объект класса CalcVolatility должен обрабатывать только один файл. А цикл по файлам должен быть вне
        #  класса, в основном коде. Это нужно, чтобы во следующих задачах без особенно больших изменений применить
        #  существующий код класса
        with open(file=full_file_name, mode='r') as file:
            for line in file:
                secid, tradetime, price, quantuty = line.split(',')
                if secid == 'SECID':
                    continue
                self.prices[secid].append(price)

    def get_volatilities(self):
        for secid, price in self.prices.items():
            min_price = min(map(float, self.prices[secid]))
            max_price = max(map(float, self.prices[secid]))
            average_price = (max_price + min_price) / 2
            volatility = ((max_price - min_price) / average_price) * 100
            return secid, round(volatility, 2)


def get_max_min_zero_vol(data):
    global secid, vol
    for secid, vol in sorted(data.items(), key=lambda para: para[1]):
        if vol == 0.0:
            zero_volatilities.append(secid)
        elif len(min_volatilities) < 3:
            min_volatilities[secid] = vol
        else:
            break
    for secid, vol in sorted(data.items(), key=lambda para: para[1], reverse=True):
        if len(max_volatilities) < 3:
            max_volatilities[secid] = vol
        else:
            break


volatilities = defaultdict(float)
max_volatilities = defaultdict(float)
min_volatilities = defaultdict(float)
zero_volatilities = []

for dirpath, dirnames, filenames in os.walk(FILE_NAME):
    for doc in filenames:
        full_file_name = os.path.join(dirpath, doc)
        volatility = CalcVolatility(full_file_name)
        volatility.get_prices()
        secid, vol = volatility.get_volatilities()
        volatilities[secid] = vol

get_max_min_zero_vol(volatilities)

print('Максимальная волатильность:')
for secid, vol in sorted(max_volatilities.items(), key=lambda para: para[1], reverse=True):
    print(f'{secid} - {vol}%')
print('Минимальная волатильность:')
for secid, vol in sorted(min_volatilities.items(), key=lambda para: para[1], reverse=True):
    print(f'{secid} - {vol}%')
print('Нулевая волатильность:')
print(', '.join(sorted(zero_volatilities)))

# зачет!
