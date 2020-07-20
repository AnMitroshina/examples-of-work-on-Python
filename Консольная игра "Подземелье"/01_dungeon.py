# -*- coding: utf-8 -*-

import datetime
import json
import logging
import re
from decimal import Decimal
from random import random, choice, choices

remaining_time = '123456.0987654321'
field_names = ['current_location', 'current_experience', 'current_date']

LOGFILE = 'log_dungeon.log'
log = logging.getLogger('dungeon')
log.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(filename=LOGFILE)
file_handler.setFormatter(logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s",
                                            datefmt="%d-%m-%Y %H:%M"))
log.addHandler(file_handler)

RE_XP = r'exp(\d+)'
RE_TIME = r'tm(\d+)'

DICT_MENU = {
    'menu_if_mobs_and_locs': ['хочу пойти дальше в подземелье - 1', 'убью монстра - 2', 'выйду отсюда нафиг - 3'],
    'menu_if_locs': ['хочу пойти дальше в подземелье - 1', 'выйду отсюда нафиг - 2'],
    'menu_if_mobs': ['убью монстра - 1', 'выйду отсюда нафиг - 2'],
    'menu_if_hatch_mob': ['попробуй разобраться с этими монстрами, но следи за временем!', 'убить монстров!! - 1']
}
DICT_MESSAGES = {'info_message': ['вы находитесь в {}. У вас {} опыта, '
                                  'а времени прошло {}:{}:'
                                  '{}:{}',
                                  'ты сейчас находишься в {}, у тебя {} опыта, '
                                  'подземелье постепенно затапливает, у тебя осталось {}'],

                 'deadlock': ['кажется ты убил всех монстров и зашел в тупик',
                              'ты не сумел набрать нужное количество очков, и тебе не хватит сил, '
                              'чтобы открыть этот люк. ты чувствуешь как вода все выше и выше. '
                              'ты делаешь последний вдох...и слышишь как подземелье шепчет:'],
                 'next_step': ['что ты будешь делать', 'твой следующий ход'],
                 'entrance': 'вход в локацию {}',
                 'mobs': ['подземный тролль {}', 'вампир {}', 'черт {}'],
                 'hatch_in_loc': ['здесь люк!', 'выход близко, наверху есть люк!'],
                 'not_enough_xp': 'у тебя не достаточно опыта {}, а нужно 280',
                 'can_open_hatch': 'ты можешь открыть люк! у тебя хватит сил и есть время',
                 'get_info': 'получить информацию - 5',
                 'step': ['убью монстра {} - {}', 'пойду в локацию {} - {}'],
                 'error': 'выбери цифры из предложенных'
                 }

class UserState:
    """
    Класс главного героя. Создается при запуске игры.
    """

    def __init__(self):
        """
        Герой создается с минимальными характеристиками
        :param location: Location_0_tm0"
        :param user_xp: Количество опыта за убийство мобов 0
        :param user_time: Время потраченное игроком
        """
        self.location = None
        self.user_xp = Decimal(0)
        self.user_time = Decimal(0)


class GameStep:
    """
    Класс с шагами игры
    """

    def __init__(self, file_name, time_limit):
        """
        :param locations: список локаций в json формате
        :param data_file: файл с информацией о локациях
        :param player: информация о игроке
        :param time_limit: время для прохождения игры
        :param game_over: флажок для окончания игры
        :param hatch: флажок для запуска сценария с люком
        :param choic_loc: список ходов из локации
        :param mobs: список монстров в локации
        :param format_t

        """
        self.data_file = file_name
        with open(self.data_file, "r") as json_file:
            self.locations = json.load(json_file)
        self.player = UserState()
        self.time_limit = time_limit
        self.game_over = False
        self.hatch = False
        self.choic_loc = []
        self.mobs = []

    def run(self):
        """Игра продолжается до тех пор, пока не установлен флаг game_over"""
        while self.game_over is False:
            if self.player.user_time <= Decimal(self.time_limit):
                self.get_data_locations()
                if self.hatch is False:
                    self.get_next_step()
                elif self.hatch is True:
                    self.open_hatch()
        print('пока-пока')

    def get_data_locations(self):
        self.choic_loc = []
        self.mobs = []
        log.debug(self.locations)
        for location, data in self.locations.items():

            self.player.location = location
            self.locations = self.locations[location]
            self.format_time = datetime.datetime(year=1, month=1, day=1) + \
                               datetime.timedelta(seconds=float(self.player.user_time))

            print(DICT_MESSAGES['info_message'][0].format(self.player.location, self.player.user_xp,
                                                          self.format_time.day, self.format_time.hour,
                                                          self.format_time.minute, self.format_time.second))

            for n in data:
                if type(n) == dict:
                    for k, v in n.items():
                        if 'Hatch' in k:
                            print(random.choices(DICT_MESSAGES['hatch_in_loc']))
                            self.hatch = True
                        else:
                            print(DICT_MESSAGES['entrance'].format(k))
                            self.choic_loc.append(k)
                elif type(n) != dict:
                    print(choice(DICT_MESSAGES['mobs']).format(n))
                    self.mobs.append(n)

    def get_next_step(self):
        """ До тех пор, пока действия происходят в одной локации повторяется запрос действий от игрока
         в рамках локации"""
        same_loc = True
        while same_loc is True:
            log.debug(f'у героя сейчас {self.player.user_time}, всего времени {self.time_limit}')
            if self.player.user_time <= Decimal(self.time_limit):
                print('================================')
                print(choices(DICT_MESSAGES['next_step'])[0])
                if self.mobs and self.choic_loc:
                    for point in DICT_MENU['menu_if_mobs_and_locs']:
                        print(point)
                    conditions = 'mobs_and_locs'
                elif self.mobs and not self.choic_loc:
                    for point in DICT_MENU['menu_if_mobs']:
                        print(point)
                    conditions = 'mobs'
                elif not self.mobs and self.choic_loc:
                    for point in DICT_MENU['menu_if_locs']:
                        print(point)
                    conditions = 'locs'
                elif not self.mobs and not self.choic_loc:
                    print(DICT_MESSAGES['deadlock'][0])
                    return self.set_game_over()

                print(DICT_MESSAGES['get_info'])
                next_step = input('выбери шаг - введите номер ')

                if next_step == '5':
                    self.get_info()
                else:
                    same_loc = self.determine_step(conditions, next_step)
            else:
                print('не понятно что делать', f'{next_step}')  # отладочный принт

    def open_hatch(self):
        while True:
            log.debug(f'у героя сейчас {self.player.user_time}, всего времени {self.time_limit}')
            self.get_info()

            if self.player.user_xp >= 280 and self.player.user_time <= Decimal(self.time_limit):
                print(DICT_MESSAGES['can_open_hatch'])
                input('открыть люк! - 1 ')
                return self.set_game_over()

            elif self.player.user_xp < 280 and self.player.user_time <= Decimal(self.time_limit):
                print(DICT_MESSAGES['not_enough_xp'].format(self.player.user_xp))

                if self.mobs:
                    for point in DICT_MENU['menu_if_hatch_mob']:
                        print(point)
                    conditions = 'mobs'
                elif not self.mobs:
                    print(DICT_MESSAGES['deadlock'])
                    return self.set_game_over()

                print(DICT_MESSAGES['get_info'])
                next_step = input('выбери шаг - введите номер ')

                if next_step == '5':
                    self.get_info()
                else:
                    self.determine_step(conditions, next_step)

    def determine_step(self, conditions, next_step):
        if conditions == 'mobs_and_locs':
            return self._mobs_and_locs_scenario(next_step)
        elif conditions == 'mobs':
            return self._mobs_scenario(next_step)
        elif conditions == 'locs':
            return self._locs_scenario(next_step)

    def _mobs_and_locs_scenario(self, next_step):
        if next_step == '1':
            return self.go_in_loc()
        elif next_step == '2':
            return self.kill_mob()
        elif next_step == '3':
            return self.set_game_over()
        else:
            print(DICT_MESSAGES['error'])
            return True


    def _mobs_scenario(self, next_step):
        if next_step == '1':
            return self.kill_mob()
        elif next_step == '2':
            return self.set_game_over()
        else:
            print(DICT_MESSAGES['error'])
            return True

    def _locs_scenario(self, next_step):
        if next_step == '1':
            return self.go_in_loc()
        elif next_step == '2':
            return self.set_game_over()
        else:
            print(DICT_MESSAGES['error'])
            return True

    def kill_mob(self):
        print('================================')
        for num, mob in enumerate(self.mobs):
            print(DICT_MESSAGES['step'][0].format(mob, num + 1))
        ind_mob = int(input('выбери монстра - введи номер ')) - 1
        mob = self.mobs[ind_mob]
        self.mobs.remove(mob)
        self.player.user_xp += Decimal(re.findall(RE_XP, mob)[0])
        self.player.user_time += Decimal(re.findall(RE_TIME, mob)[0])
        return True

    def go_in_loc(self):
        print('================================')
        for num, loc in enumerate(self.choic_loc):
            print(DICT_MESSAGES['step'][1].format(loc, num + 1))
        index_next_loc = int(input('выбери локацию  - введите номер ')) - 1
        for num, loc in enumerate(self.locations):
            if type(loc) == dict and self.choic_loc[index_next_loc] in loc.keys():
                self.locations = self.locations[num]
                self.player.user_time += Decimal(re.findall(RE_TIME, self.choic_loc[index_next_loc])[0])
                print(self.player.user_time)
                return False

    def get_info(self):
        delta = float(Decimal(self.time_limit) - Decimal(self.player.user_time))
        delta_sec = datetime.timedelta(seconds=delta)
        hours_min_sec = datetime.datetime(1, 1, 1) + delta_sec
        current_time = f'{hours_min_sec.hour}:{hours_min_sec.minute}:{hours_min_sec.second}'
        print(DICT_MESSAGES['info_message'][1].format(self.player.location, self.player.user_xp, current_time))

        log.debug(f'время пользователя: {self.player.user_time}, оставшееся время {delta}')

    def set_game_over(self):
        self.game_over = True
        return False


# Учитывая время и опыт, не забывайте о точности вычислений!


if __name__ == '__main__':
    a = GameStep('rpg.json', time_limit=remaining_time)
    a.run()

# зачет!
