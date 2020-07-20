# -*- coding: utf-8 -*-


# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Skillbox Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png
# Пример заполнения lesson_013/images/ticket_sample.png
# Подходящий шрифт искать на сайте ofont.ru

TEMPLATE_FILE_NAME = '/Users/annushka/PycharmProjects/python_base/python_base/lesson_013/images/ticket_template.png'
FONT_FILE_NAME = '/Users/annushka/PycharmProjects/python_base/python_base/lesson_013/ofont_ru_Tengri.ttf'
SAVE_TO = 'My_ticket.png'

from PIL import Image, ImageDraw, ImageFont, ImageColor


def make_ticket(fio, from_, to, date):
    template_ticket = Image.open(TEMPLATE_FILE_NAME)

    width, high = template_ticket.size
    draw = ImageDraw.Draw(template_ticket)
    font = ImageFont.truetype(font=FONT_FILE_NAME, size=16)

    message = '{}'.format(fio)
    y = high - 274
    draw.text((45, y), message, font=font, fill=ImageColor.colormap['black'])

    message = "{}".format(from_)
    y = high - 204
    draw.text((45, y), message, font=font, fill=ImageColor.colormap['black'])

    message = "{}".format(to)
    y = high - 138
    draw.text((45, y), message, font=font, fill=ImageColor.colormap['black'])

    font = ImageFont.truetype(font=FONT_FILE_NAME, size=14)
    message = "{}".format(date)
    y = high - 136
    draw.text((287, y), message, font=font, fill=ImageColor.colormap['black'])
    template_ticket.save(SAVE_TO)


make_ticket('Ivanov', 'Moscow', 'Rim', '20.10')

# зачет! 
