# -*- coding: utf-8 -*-

from random import randint, choice

# Доработать практическую часть урока lesson_007/python_snippets/08_practice.py - не могу сделать импорт
# https://prnt.sc/r1zpgi
#  У меня работает так: (насколько я помню документацию, имя модуля не должно начинаться с числа, как и
#  имя любой другой переменной, функции, класса...
#  документация питона? я не нашла там информации
#  https://docs.python.org/3/reference/simple_stmts.html#the-import-statement
#  и еще такой вопрос, на данном этапе должно уже формироваться понимания о том, как взаимосвязано создание классов
#  и то, сколько они места занимают в системе ком-ра?
#  Это самый первый модуль где вы встретили ООП, следовательно, вы только знакомитесь с этой темой. Далее она будет
#  развиваться, в следующем модуле будут взаимосвязи объектов, а в 9м - паттерны проектирования на основе ООП
# TODO Александр, большое спасибо за метариалы!

# Необходимо создать класс кота. У кота есть аттрибуты - сытость - есть и дом (в котором он живет) - есть
# Кот живет с человеком в доме.
# Для кота дом характеризируется - миской для еды и грязью.
# Изначально в доме нет еды для кота и нет грязи.

# Доработать класс человека, добавив методы
#   подобрать кота - у кота появляется дом. - есть
#   купить коту еды - кошачья еда в доме увеличивается на 50, деньги уменьшаются на 50. есть
#   убраться в доме - степень грязи в доме уменьшается на 100, сытость у человека уменьшается на 20. done
# Увеличить кол-во зарабатываемых человеком денег до 150 (он выучил пайтон и устроился на хорошую работу :) done

# Кот может есть, спать и драть обои - необходимо реализовать соответствующие методы.
# Когда кот спит - сытость уменьшается на 10 done
# Когда кот ест - сытость увеличивается на 20, кошачья еда в доме уменьшается на 10. done
# Когда кот дерет обои - сытость уменьшается на 10, степень грязи в доме увеличивается на 5 есть
# Если степень сытости < 0, кот умирает.
# Так же надо реализовать метод "действуй" для кота, в котором он принимает решение
# что будет делать сегодня

# Человеку и коту надо вместе прожить 365 дней.

from termcolor import cprint


class Man:

    def __init__(self, name):
        self.name = name
        self.fullness = 50
        self.house = None
        self.cat = None

    def __str__(self):
        return 'Я - {}, сытость {}'.format(
            self.name, self.fullness)

    def eat(self):
        if self.house.food >= 10:
            cprint('{} поел'.format(self.name), color='yellow')
            self.fullness += 10
            self.house.food -= 10
        else:
            cprint('{} нет еды'.format(self.name), color='red')

    def work(self):
        cprint('{} сходил на работу'.format(self.name), color='blue')
        self.house.money += 150
        self.fullness -= 10

    def watch_MTV(self):
        if self.house.dirty < 60:
            cprint('{} смотрел MTV целый день'.format(self.name), color='green')
            self.fullness -= 10
        else:
            cprint('{} не может расслабиться в этом сраче'.format(self.name), color='red')

    def shopping(self):
        if self.house.money >= 50:
            cprint('{} сходил в магазин за едой'.format(self.name), color='magenta')
            self.house.money -= 50
            self.house.food += 50
        else:
            cprint('{} деньги кончились!'.format(self.name), color='red')

    def go_to_the_house(self, house):
        self.house = house
        self.fullness -= 10
        cprint('{} Вьехал в дом'.format(self.name), color='cyan')

    def buy_cat_food(self):
        if self.house.money >= 50:
            if len(self.house.house_residents) >= 4:
                cprint('{} Купил корм семейству кошачьих'.format(self.name), color='grey')
                self.house.cat_food += 100
                self.house.money -= 100
            else:
                cprint('{} Купил корм семейству кошачьих'.format(self.name), color='grey')
                self.house.cat_food += 50
                self.house.money -= 50
        else:
            cprint('Денег нет, {}!(', color='red')

    def clean_house(self):
        if self.fullness > 20 and self.house.dirty > 0:
            cprint('{} отдраил дом!'.format(self.name), color='white')
            self.house.dirty -= 100
            self.fullness -= 20
        elif self.house.dirty <= 0:
            cprint('Дом чист!', color='white')
        else:
            cprint('{} слишком голоден для бешенной чистки!'.format(self.name), color='red')

    def take_cat(self, cat):
        self.house.cat_food += 50
        self.cat = cat
        self.house.money -= 50
        self.house.house_residents.append(cat)
        cprint('{} взял кота, и назвал его {}'.format(self.name, self.cat.name), 'red', attrs=['dark'])

    def act(self):
        if self.fullness <= 0:
            cprint('{} умер...'.format(self.name), color='red')
            return
        dice = randint(1, 6)
        if self.fullness <= 20:
            self.eat()
        elif self.house.food <= 10:
            self.shopping()
        elif self.house.money <= 50:
            self.work()
        elif self.house.cat_food <= 10 and len(self.house.house_residents) < 4:
            self.buy_cat_food()
        elif self.house.cat_food <= 80 and len(self.house.house_residents) >= 4:
            self.buy_cat_food()
        elif self.house.cat_food <= 100 and len(self.house.house_residents) >= 8:
            self.buy_cat_food()
        elif self.house.dirty > 60:
            self.clean_house()
        elif dice == 1:
            self.work()
        elif dice == 2:
            self.eat()
        elif dice == 3:
            self.clean_house()
        else:
            self.watch_MTV()


class House:
    house_residents = []

    def __init__(self):
        self.food = 50
        self.money = 0
        self.dirty = 0
        self.cat_food = 0

    def __str__(self):
        return 'В доме еды осталось {}, денег осталось {}, загрязненность стала {}, еда для котиков {}'.format(
            self.food, self.money, self.dirty, self.cat_food)


class Cat:

    def __init__(self, name, house):
        self.house = house
        self.full = 0
        self.name = name
        self.man = None

    def get_full_stomach(self):
        if self.house.cat_food >= 10:
            cprint('{} поглащает еду'.format(self.name), 'red', attrs=['dark'])
            self.full += 20
            self.house.cat_food -= 10
        else:
            self.full -= 5
            cprint('У питомцев нет еды.', color='red')

    def sleep(self):
        if self.full > 10:
            cprint('{} спит'.format(self.name), 'red', attrs=['dark'])
            self.full -= 10
        else:
            cprint('{} не может уснуть от голода'.format(self.name), color='red')

    def __str__(self):
        return 'состояние {}: сытость {}'.format(self.name, self.full)

    def tear_wallpaper(self):
        if self.full > 10:
            cprint('{} точит когти...об обои. КУПИ КОГТЕТОЧКУ'.format(self.name), 'red', attrs=['dark'])
            self.full -= 10
            self.house.dirty += 5
        else:
            cprint('{} настолько голоден, что не может шалить(('.format(self.name), color='red')

    def weird_act(self):
        acts = ['смотрит в стену', 'охотится за бликами солнца', 'пытается поймать свой хвост',
                'следит за другими жителями дома']
        if self.full > 10:
            self.full -= 10
            cprint('{} {}'.format(self.name, choice(acts)), 'yellow', attrs=['blink'])
        else:
            cprint('{} настолько голоден, что не может шалить(('.format(self.name), color='red')

    def act(self):
        dice = randint(1, 6)
        if self.full <= 10:
            self.get_full_stomach()
        elif self.full < 0:
            cprint('{} скончался :( !'.format(self.name))
            self.house.house_residents.remove(cat)
            return
        elif dice == 1:
            self.get_full_stomach()
        elif dice == 2:
            self.tear_wallpaper()
        elif dice == 3:
            self.weird_act()
        else:
            self.sleep()


dict_of_cat_names_fedor = {
    "bedolaga": 'Бедолага',
    'captain_coco': 'Капитан Кокс',
    'admiral_kruzenstern': 'Адмирал Крузенштерн',
    'godfather': 'Крестный Отец',
    'pugovka': 'Пуговка',
    'kukuruzinka': 'Кукурузинка',
    'aleshka': 'Алешка',
    'Mishka': 'Мышка',
    'Markiza': 'Маркиза',
    'Volk': 'Волк',
    'Korol': 'Король',
    'Kony': 'Конь'
}
cat_names_keys = list(dict_of_cat_names_fedor.keys())
my_home = House()
fedot = Man('Федот')
fedot.go_to_the_house(house=my_home)
my_home.house_residents.append(fedot)
for day in range(1, 366):
    print('================ день {} =================='.format(day))
    if (len(my_home.house_residents)-1) * 20 <= my_home.cat_food and (len(my_home.house_residents)-1) * 20 <= \
            my_home.money and my_home.dirty <= 10:
        if not cat_names_keys:
            print('Я бы взял кота, но фантазия на имена кончилась')
        else:
            cat_name = choice(cat_names_keys)
            cat_names_keys.remove(cat_name)
            cat = Cat(name=dict_of_cat_names_fedor[cat_name], house=my_home)
            fedot.take_cat(cat=cat)
    for resident in my_home.house_residents:
        resident.act()
    print('--- в конце дня ---')
    for resident in my_home.house_residents:
        print(resident)
    print(my_home)
print('Максимум кошек может быть: {}'.format(len(my_home.house_residents)-1))

# Усложненное задание (делать по желанию)
# Создать несколько (2-3) котов и подселить их в дом к человеку.
# Им всем вместе так же надо прожить 365 дней.

# (Можно определить критическое количество котов, которое может прокормить человек...)

# зачет!
