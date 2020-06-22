TOKEN = '7a73d53386dcf8c0f43c65f51ede4226df7e00a8c422b793861538c558fe7d7f46cf19d91d894be1bd1f2'
GROUP_ID = 192930826

INTENT = [
    {
        'name': 'Дата проведения',
        'tokens': ('когда', 'сколько', 'дата', 'дату'),
        'scenario': None,
        'answer': 'Конференция проводится 9 мая, регистрация начнется в 10 утра'
    },
    {
        'name': 'Место проведения',
        'tokens': ('где', 'место', 'локация', 'адрес', 'метро'),
        'scenario': None,
        'answer': 'Конференция пройдет на Красной Площади, около Ленина'
    },
    {
        'name': 'Регистрация',
        'tokens': ('регист', 'добави'),
        'scenario': 'registration',
        'answer': None
    }
]

SCENARIOS = {
    'registration': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'Чтобы зарегистрироваться, введите ваше имя. Оно будет написано на бейджике.',
                'failure_text': 'Имя должно состоять из 3-30 букв и дефиса. Попробуйте еще раз',
                'handler': 'handler_name',
                'next_step': 'step2',
            },
            'step2': {
                'text': 'Введите e-mail. Мы отправим на него все данные',
                'failure_text': 'Во введеном адресе ошибка. Попробуйте еще раз',
                'handler': 'handler_email',
                'next_step': 'step3'
            },
            'step3': {
                'text': 'Спасибо за регистрацию, {name}! Мы отправили на {email} билет, распечатайте его.',
                'image': 'handler_generate_ticket',
                'failure_text': None,
                'handler': None,
                'next_step': None
            }
        }
    }}

DEFAULT_ANSWERS = 'Не знаю как на это ответить.' \
                  'Могу сказать когда и где пройдет конференция, а также зарегистрировать вас, просто спросите.'

DB_CONFIG = dict(
    provider='postgres',
    user='postgres',
    host='localhost',
    database='vk_chat_bot'
    )