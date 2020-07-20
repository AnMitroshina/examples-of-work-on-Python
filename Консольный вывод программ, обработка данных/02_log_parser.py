# -*- coding: utf-8 -*-

# Имеется файл events.txt вида:
#
# [2018-05-17 01:55:52.665804] NOK
# [2018-05-17 01:56:23.665804] OK
# [2018-05-17 01:56:55.665804] OK
# [2018-05-17 01:57:16.665804] NOK
# [2018-05-17 01:57:58.665804] OK
# ...
#
# Напишите программу, которая считывает файл
# и выводит число событий NOK за каждую минуту в другой файл в формате
#
# [2018-05-17 01:57] 1234
# [2018-05-17 01:58] 4321
# ...
#
# Входные параметры: файл для анализа, файл результата
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.
# После выполнения первого этапа нужно сделать группировку событий
#  - по часам
#  - по месяцу
#  - по году
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828

import zipfile

FILE_IN = 'events.txt'
FILE_OUT = 'file_out'


class TreatmentLog:

    def __init__(self, name_file_in, name_file_out=None):
        self.file_in = name_file_in
        self.file_out = name_file_out
        self.done_lines = {}
        self.number_characters = None

    def get_result_file(self):
        self.set_stat_mark()
        self.get_stat()
        self.get_statistic_file()

    def set_stat_mark(self):
        pass

    def unzip(self):
        zfile = zipfile.ZipFile(self.file_in, 'r')
        for filename in zfile.namelist():
            zfile.extract(filename)
        self.file_in = filename

    def get_stat(self):
        if self.file_in.endswith('.zip'):
            self.unzip()
        with open(file=self.file_in, mode='r', encoding='cp1251') as file:
            for line in file:
                if 'NOK' in line:
                    new_line = line[:self.number_characters] + ']'
                    if new_line in self.done_lines:
                        self.done_lines[new_line] += 1
                    else:
                        self.done_lines[new_line] = 1

    def get_statistic_file(self):
        with open(file=self.file_out, mode='w', encoding='utf8') as file:
            for date, count in self.done_lines.items():
                file.write('{} {}'.format(date, count))
                file.write('\n')


class StatisticsMinutes(TreatmentLog):

    def set_stat_mark(self):
        self.number_characters = 17


class StatisticsHours(TreatmentLog):

    def set_stat_mark(self):
        self.number_characters = 14


class StatisticsDays(TreatmentLog):

    def set_stat_mark(self):
        self.number_characters = 11


class StatisticsMonths(TreatmentLog):

    def set_stat_mark(self):
        self.number_characters = 8


class StatisticsYears(TreatmentLog):

    def set_stat_mark(self):
        self.number_characters = 5

test_1 = StatisticsMinutes(FILE_IN, FILE_OUT)
test_1.get_result_file()
# test_2 = StatisticsHours(FILE_IN, FILE_OUT)
# test_2.get_result_file()
# test_3 = StatisticsDays(FILE_IN, FILE_OUT)
# test_3.get_result_file()
# test_4 = StatisticsMonths(FILE_IN, FILE_OUT)
# test_4.get_result_file()

# зачет!
