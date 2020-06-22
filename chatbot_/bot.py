#!/Users/annushka/PycharmProjects/python_base/python_base/chatbot_ python3
import requests
from pony.orm import db_session

from models import UserState, Registration
from settings import TOKEN, GROUP_ID
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from random import randint
import logging

import _handlers as _handlers

try:
    import settings as settings
except ImportError:
    exit('DO cp settings.py.default settings.py and set TOKEN!')

LOGFILE = 'logbot.log'
log = logging.getLogger('BoT')
log.setLevel(logging.DEBUG)


def configure_logging():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler(filename=LOGFILE)
    file_handler.setFormatter(logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s",
                                                datefmt="%d-%m-%Y %H:%M"))
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)


class Bot:
    """
    Echo bot для социальной сети в вк
    Used python 3.7"""

    def __init__(self, group_id, token):
        """

        :param group_id: id группы в ВК
        :param token: секретный токен из группы ВК
        """
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()

    def run(self):
        """
        Запуск бота
        """
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception('Ошибка в обработке события')

    @db_session
    def on_event(self, event):
        """
        Отправляет сообщение назад, если это текст
        :param event: VkBotMessageEvent object
        :return: None
        """
        log.debug('получено событие')

        if event.type != VkBotEventType.MESSAGE_NEW:
            log.info(f'мы пока не умеем обрабатывать событие такого типы {event.type}')
            return

        user_id = event.object.message['from_id']
        text = event.object.message["text"]

        state = UserState.get(user_id=str(user_id))
        # user_id = event.object.message['user_id']

        if state is not None:
            self.continue_scenario(text=text, state=state, user_id=user_id)

        else:
            # search intent
            for intent in settings.INTENT:
                log.debug(f'User gets {intent}')
                if any(token in text.lower() for token in intent['tokens']):
                    if intent['answer']:
                        self.send_to_text(peer_id=user_id, text_to_send=intent['answer'])
                    # run intent
                    else:
                        self.start_scenario(scenario_name=intent['scenario'], text=text, user_id=user_id)  # если у
                        # интента нет ответа - значит мы запускаем сценарий регистрации
                    break
            else:
                self.send_to_text(peer_id=user_id, text_to_send=settings.DEFAULT_ANSWERS)  # если у интента нет
                # подходящего токена, вовращается заглушка

    def send_to_text(self, peer_id, text_to_send):
        self.api.messages.send(message=text_to_send,
                               random_id=randint(0, 2 ** 20),
                               peer_id=peer_id,
                               )

    def send_image(self, image, user_id):
        upload_url = self.api.photos.getMessagesUploadServer()['upload_url']
        upload_date = requests.post(url=upload_url, files={'photo': ('img.png', image, 'img/png')}).json()
        print(upload_date)
        image_data = self.api.photos.saveMessagesPhoto(**upload_date)
        owner_id = image_data[0]['owner_id']
        media_id = image_data[0]['id']

        attachment = f'photo{owner_id}_{media_id}'
        self.api.messages.send(attachment=attachment,
                               random_id=randint(0, 2 ** 20),
                               peer_id=user_id,
                               )

    def sent_step(self, step, user_id, text, context):
        if 'text' in step:
            self.send_to_text(user_id, step['text'].format(**context))
        if 'image' in step:
            handler = getattr(_handlers, step['image'])
            image = handler(text, context)
            self.send_image(user_id=user_id, image=image)

    def start_scenario(self, scenario_name, user_id, text):
        scenario = settings.SCENARIOS[scenario_name]  # 'registration'
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]  # 'step1'
        self.sent_step(step, user_id, text, context={})
        UserState(user_id=str(user_id), scenario_name=scenario_name, step_name=first_step,
                  context={})  # создаем состояние пользователя записываем в бд

    def continue_scenario(self, text, state, user_id):
        steps = settings.SCENARIOS[state.scenario_name]['steps']  # в данном случае 'registration'
        step = steps[state.step_name]
        handler = getattr(_handlers, step['handler'])  # из модуля _handlers возвращается соответствующая ф-я
        if handler(text=text, context=state.context):
            next_step = steps[step['next_step']]
            self.sent_step(next_step, user_id, text, state.context)
            if next_step['next_step']:
                # switch next step
                state.step_name = step['next_step']
            else:
                # finish scenario
                Registration(name=state.context['name'], email=state.context['email'])
                state.delete()
        else:
            text_to_send = step['failure_text'].format(**state.context)
            self.send_to_text(user_id, text_to_send)


if __name__ == '__main__':
    configure_logging()
    bot = Bot(group_id=GROUP_ID, token=TOKEN)
    bot.run()

# зачет
