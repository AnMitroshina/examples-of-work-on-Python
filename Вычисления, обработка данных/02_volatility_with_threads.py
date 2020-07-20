# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПОТОЧНОМ стиле
#
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
import os
from collections import defaultdict
from threading import Thread

FILE_NAME = 'trades'
volatilities = defaultdict(float)
max_volatilities = defaultdict(float)
min_volatilities = defaultdict(float)
zero_volatilities = []


class CalcVolatility(Thread):

    def __init__(self, file_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_name = file_name
        self.prices = defaultdict(list)

    def run(self):
        self.get_prices()
        self.get_volatilities()

    def get_prices(self):
        with open(file=self.file_name, mode='r') as file:
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
            self.volatility = ((max_price - min_price) / average_price) * 100
            self.volatility = round(self.volatility, 2)
            self.secid = secid
            return self.secid, self.volatility


def get_max_min_zero_vol(data):
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


def get_vols(main_file_name):
    full_files_names = []

    for dirpath, dirnames, filenames in os.walk(main_file_name):
        for doc in filenames:
            full_files_names.append(os.path.join(dirpath, doc))
    """Один файл разбирает поток""" # TODO разве я здесь не создаю потоки? у одного потока - свой файл, соответственно они
    # не мешают друг другу, и выносить что-либо из класса - не имеет смысла, т.к. класс изначально писался под один
    # поток
    tickers = [CalcVolatility(file_name=full_name) for full_name in full_files_names]
    for ticker in tickers:
        ticker.start()
    for ticker in tickers:
        ticker.join()

    for ticker in tickers:
        volatilities[ticker.secid] = ticker.volatility
    return volatilities


get_vols(FILE_NAME)
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
