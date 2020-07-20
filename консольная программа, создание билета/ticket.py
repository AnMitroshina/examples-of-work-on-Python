# -*- coding: utf-8 -*-


# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Skillbox Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png
# Пример заполнения lesson_013/images/ticket_sample.png
# Подходящий шрифт искать на сайте ofont.ru

# Усложненное задание (делать по желанию).
# Написать консольный скрипт c помощью встроенного python-модуля agrparse.
# Скрипт должен принимать параметры:
#   --fio - обязательный, фамилия.
#   --from - обязательный, откуда летим.
#   --to - обязательный, куда летим.
#   --date - обязательный, когда летим.
#   --save_to - необязательный, путь для сохранения заполненнего билета.
# и заполнять билет.

from PIL import Image, ImageDraw, ImageFont, ImageColor
import argparse


TEMPLATE_FILE_NAME = '/Users/annushka/PycharmProjects/python_base/python_base/lesson_013/images/ticket_template.png'
FONT_FILE_NAME = '/Users/annushka/PycharmProjects/python_base/python_base/lesson_013/ofont_ru_Tengri.ttf'


def make_ticket(args):

    template_ticket = Image.open(TEMPLATE_FILE_NAME)

    width, high = template_ticket.size
    draw = ImageDraw.Draw(template_ticket)
    font = ImageFont.truetype(font=FONT_FILE_NAME, size=16)

    message = '{}'.format(args.fio)
    y = high - 274
    draw.text((45, y), message, font=font, fill=ImageColor.colormap['black'])

    message = "{}".format(args.from_)
    y = high - 204
    draw.text((45, y), message, font=font, fill=ImageColor.colormap['black'])

    message = "{}".format(args.to)
    y = high - 138
    draw.text((45, y), message, font=font, fill=ImageColor.colormap['black'])

    font = ImageFont.truetype(font=FONT_FILE_NAME, size=14)
    message = "{}".format(args.date)
    y = high - 138
    draw.text((287, y), message, font=font, fill=ImageColor.colormap['black'])
    template_ticket.save(args.save_to)


parser = argparse.ArgumentParser(description='fill out a ticket')
parser.add_argument('--fio', type=str, help='example: Ivanov I.I.')
parser.add_argument('--from_', type=str, help='example: Moscow')
parser.add_argument('--to', type=str, help='example: Rim')
parser.add_argument('--date', type=str, help='example: 12.09')
parser.add_argument('--save_to', type=str, default='my_ticket.png', help='example: my_ticket.png')

args = parser.parse_args()
make_ticket(args)

