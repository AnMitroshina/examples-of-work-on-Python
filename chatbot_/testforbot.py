import unittest
from copy import deepcopy
from unittest import TestCase
from unittest.mock import patch, Mock, ANY

from pony.orm import db_session, rollback
from vk_api.bot_longpoll import VkBotMessageEvent, VkBotEvent

import _handlers as _handlers
import settings as settings
from bot import Bot
from models import UserState
from ticket_user import user_ticket


def isolate_db(test_func):
    def wrapper(*args, **kwargs):
        with db_session:
            test_func(*args, **kwargs)
            rollback()

    return wrapper


class TestBot(TestCase):
    ROW_EVENT = {'type': 'message_new',
                 'object': {'message': {'date': 1584359515, 'from_id': 587091303, 'id': 115,
                                        'out': 0, 'peer_id': 587091303, 'text': 'ыва', 'conversation_message_id': 112,
                                        'fwd_messages': [], 'important': False, 'random_id': 0, 'attachments': [],
                                        'is_hidden': False},
                            'client_info': {'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link'],
                                            'keyboard': True, 'inline_keyboard': True, 'lang_id': 3}},
                 'group_id': 192930826, 'event_id': 'aece44287a236aa1335dbf552f74343e196d7356'}

    def test_run(self):
        count = 5
        obj = {'a': 1}
        events = [obj] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock
        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot('', '')
                bot.on_event = Mock()
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_any_call(obj)
                assert bot.on_event.call_count == 5

    def test_on_event(self):
        # TODO не понимаю почему тест остался в рабочем состоянии, возможно я его в принципе не правильно написала
        """проверить работу каждой функции на каждый step"""
        event = VkBotMessageEvent(raw=self.ROW_EVENT)
        send_mock = Mock()
        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll'):
                bot = Bot('', '')
                bot.api = Mock()
                text = settings.DEFAULT_ANSWERS
                bot.api.messages.send = send_mock
                bot.on_event(event=event)
        send_mock.assert_called_once_with(message=text,
                                          random_id=ANY,
                                          peer_id=self.ROW_EVENT['object']['message']['peer_id']
                                          )

    INPUTS = [
        'Привет',
        'А когда будет',
        'Где будет проходит конференция?',
        'Зарегистрируй меня',
        'TEST',
        'Мой адрес test@test',
        'test@test.ru'
    ]
    EXPECTED_OUTPUTS = [
        settings.DEFAULT_ANSWERS,
        settings.INTENT[0]['answer'],
        settings.INTENT[1]['answer'],
        settings.SCENARIOS['registration']['steps']['step1']['text'],
        settings.SCENARIOS['registration']['steps']['step2']['text'],
        settings.SCENARIOS['registration']['steps']['step2']['failure_text'],
        settings.SCENARIOS['registration']['steps']['step3']['text'].format(name='TEST', email='test@test.ru')
    ]

    def test_run_ok(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock

        events = []

        for input_text in self.INPUTS:
            event = deepcopy(self.ROW_EVENT)
            event['object']['message']['text'] = input_text
            events.append(VkBotMessageEvent(event))

        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)

        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll', return_value=long_poller_mock):
                bot = Bot('', '')
                bot.api = api_mock
                bot.run()
        assert send_mock.call_count == len(self.INPUTS)

        real_outputs = []
        for call in send_mock.call_args_list:
            args, kwargs = call
            real_outputs.append(kwargs['message'])

        assert real_outputs == self.EXPECTED_OUTPUTS

    def test_image_generetion(self):
        with open('files/avatar_test.png', 'rb') as f:
            avatar_mock = Mock()
            avatar_mock.content = f.read()

        with patch('requests.get', return_value=avatar_mock):
            ticket_file = user_ticket('test_name', 'test@test.ru')
            ticket_file_bytes = ticket_file.read()

        with open('files/user_ticket_test.png', 'rb') as expected_file:
            expected_bytes = expected_file.read()

        assert ticket_file_bytes == expected_bytes


if __name__ == '__main__':
    unittest.main()

# зачет!
