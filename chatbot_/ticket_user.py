from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont

TEMPLATE = 'files/template_ticket.png'
FONT = 'files/Roboto-Regular.ttf'
FONT_SIZE = 20
BLACK = (0, 0, 0, 255)
NAME_COORDINATE = (330, 230)
EMAIL_COORDINATE = (330, 275)
AVATAR_SIZE = 100
AVATAR_OFFSET = (100, 220)


def user_ticket(name, email):
    template_ticket = Image.open(TEMPLATE).convert('RGBA')
    draw = ImageDraw.Draw(template_ticket)
    font = ImageFont.truetype(font=FONT, size=20)
    draw.text(NAME_COORDINATE, name, font=font, fill=BLACK)
    draw.text(EMAIL_COORDINATE, email, font=font, fill=BLACK)

    response = requests.get(f'https://api.adorable.io/avatars/{AVATAR_SIZE}/{email}')
    avatar_file_like = BytesIO(response.content)
    avatar = Image.open(avatar_file_like)
    template_ticket.paste(avatar, AVATAR_OFFSET)

    temp_file = BytesIO()
    template_ticket.save(temp_file, 'png')
    temp_file.seek(0)

    return temp_file


