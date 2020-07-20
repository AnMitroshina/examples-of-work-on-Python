# -*- coding: utf-8 -*-

import zipfile
from abc import abstractmethod
from pprint import pprint

# Подсчитать статистику по буквам в романе Война и Мир.
# Входные параметры: файл для сканирования
# Статистику считать только для букв алфавита (см функцию .isalpha() для строк)
#
# Вывести на консоль упорядоченную статистику в виде
# +---------+----------+
# |  буква  | частота  |
# +---------+----------+
# |    А    |   77777  |
# |    Б    |   55555  |
# |   ...   |   .....  |
# |    a    |   33333  |
# |    б    |   11111  |
# |   ...   |   .....  |
# +---------+----------+
# |  итого  | 9999999  |
# +---------+----------+
#
# Упорядочивание по частоте - по убыванию. Ширину таблицы подберите по своему вкусу
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.
# После выполнения первого этапа нужно сделать упорядочивание статистики
#  - по частоте по возрастанию
#  - по алфавиту по возрастанию
#  - по алфавиту по убыванию
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828
MAIN_FILE = '/Users/annushka/PycharmProjects/python_base/python_base/lesson_009/python_snippets/voyna-i-mir.txt.zip'


class Statistics:

    def __init__(self, file_name):
        self.file_name = file_name
        self.stat_chars = {}
        self.data_sort = []
        self.total_value = 0

    def result_stat(self):
        self.get_stat()
        self.sort_stat()
        self.print_stat()

    def print_stat(self):
        print('|', '-' * 59, '|')
        print('|{txt:^30}|{txt_2:^30}|'.format(txt='Буква', txt_2='Частота'))
        print('|', '-' * 59, '|')
        for para in self.data_sort:
            print('|{txt:^30}|{txt_2:^30}|'.format(txt=para[0], txt_2=para[1]))
        print('|', '-' * 59, '|')
        print('|{txt:^30}|{txt_2:^30}|'.format(txt='Итого', txt_2=self.total_value))
        print('|', '-' * 59, '|')

    def unzip(self):
        zfile = zipfile.ZipFile(self.file_name, 'r')
        for filename in zfile.namelist():
            zfile.extract(filename)
        self.file_name = filename

    def get_stat(self):
        if self.file_name.endswith('.zip'):
            self.unzip()
        with open(file=self.file_name, mode='r', encoding='cp1251') as file:
            for line in file:
                for char in line:
                    if char in self.stat_chars and char.isalpha():
                        self.stat_chars[char] += 1
                    elif char not in self.stat_chars and char.isalpha():
                        self.stat_chars[char] = 1

    def sort_stat(self):
        pass


class FrequencyIncrease(Statistics):

    def sort_stat(self):
        for char, value in sorted(self.stat_chars.items(), key=lambda number: number[1], reverse=True):
            para = (char, value)
            self.total_value += value
            self.data_sort.append(para)


class AlphabetIncrease(Statistics):

    def sort_stat(self):
        for char, value in sorted(self.stat_chars.items(), key=lambda letter: letter[0], reverse=False):
            para = (char, value)
            self.total_value += value
            self.data_sort.append(para)


class AlphabetDecrease(Statistics):

    def sort_stat(self):
        for char, value in sorted(self.stat_chars.items(), key=lambda letter: letter[0], reverse=True):
            para = (char, value)
            self.total_value += value
            self.data_sort.append(para)


alph_stat = FrequencyIncrease(file_name=MAIN_FILE)
alph_stat.result_stat()

# зачет!
