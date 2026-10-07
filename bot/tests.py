"""Тесты обработчиков Telegram-бота: рассылка заявок группе и кругу пользователей."""
from types import SimpleNamespace
from unittest import mock

# Токен нужен telebot ещё при импорте bot_instance; env уже собран при django.setup,
# поэтому подменяем значение в готовой модели, а не в os.environ
from common.config import env  # noqa: E402

env.BOT_TOKEN = '123456:UNITTEST'

from django.test import SimpleTestCase  # noqa: E402
from telebot.apihelper import ApiTelegramException  # noqa: E402

from bot import handlers  # noqa: E402
from bot.bot_instance import configs  # noqa: E402


def make_message(user_id):
    return SimpleNamespace(
        from_user=SimpleNamespace(id=user_id),
        chat=SimpleNamespace(id=user_id),
        text='привет',
    )


class SendMessageToGroupTest(SimpleTestCase):
    @mock.patch.object(handlers, 'bot')
    def test_sends_to_group_and_users(self, bot_mock):
        api = handlers.SiteMsgAPI()
        with mock.patch.object(configs, 'notification_targets', return_value=['-grp', '111']):
            api.send_message_to_group('Иван', 'Тема', 'Текст')
        expected = 'Сообщение от Иван:\nТема: Тема\nТекст'
        bot_mock.send_message.assert_any_call('-grp', expected)
        bot_mock.send_message.assert_any_call('111', expected)
        self.assertEqual(bot_mock.send_message.call_count, 2)

    @mock.patch.object(handlers, 'bot')
    def test_failed_recipient_does_not_break_others(self, bot_mock):
        bot_mock.send_message.side_effect = [
            ApiTelegramException('sendMessage', 400, {
                'ok': False, 'error_code': 400, 'description': 'Bad Request',
            }),
            None,
        ]
        api = handlers.SiteMsgAPI()
        with mock.patch.object(configs, 'notification_targets', return_value=['-grp', '111']):
            api.send_message_to_group('Иван', 'Тема', 'Текст')
        self.assertEqual(bot_mock.send_message.call_count, 2)


class SendWelcomeTest(SimpleTestCase):
    @mock.patch.object(handlers, 'bot')
    def test_admin_greeting(self, bot_mock):
        with mock.patch.object(configs, 'admin_user_ids', ['111']):
            handlers.send_welcome(make_message(111))
        self.assertIn('администратор', bot_mock.reply_to.call_args[0][1])

    @mock.patch.object(handlers, 'bot')
    def test_stranger_greeting(self, bot_mock):
        with mock.patch.object(configs, 'admin_user_ids', ['111']):
            handlers.send_welcome(make_message(222))
        self.assertIn('бот', bot_mock.reply_to.call_args[0][1])


class FetchMessagesTest(SimpleTestCase):
    @mock.patch.object(handlers, 'bot')
    @mock.patch.object(handlers, 'SiteMsgAPI')
    def test_admin_fetches_and_distributes(self, api_cls, bot_mock):
        api_cls.return_value.get_messages.return_value = [
            {'name': 'Иван', 'subject': 'Заявка', 'body': 'Текст'},
            {'name': 'Пётр', 'subject': 'Заявка 2', 'body': 'Текст 2'},
        ]
        with mock.patch.object(configs, 'admin_user_ids', ['111']):
            handlers.fetch_messages(make_message(111))
        self.assertEqual(api_cls.return_value.send_message_to_group.call_count, 2)
        api_cls.return_value.send_message_to_group.assert_any_call('Иван', 'Заявка', 'Текст')
        self.assertIn('Разослано заявок: 2', bot_mock.reply_to.call_args[0][1])

    @mock.patch.object(handlers, 'bot')
    @mock.patch.object(handlers, 'SiteMsgAPI')
    def test_non_admin_ignored(self, api_cls, bot_mock):
        with mock.patch.object(configs, 'admin_user_ids', ['111']):
            handlers.fetch_messages(make_message(222))
        api_cls.return_value.get_messages.assert_not_called()
        bot_mock.reply_to.assert_not_called()

    @mock.patch.object(handlers, 'bot')
    @mock.patch.object(handlers, 'SiteMsgAPI')
    def test_api_error_reported_to_admin(self, api_cls, bot_mock):
        import requests
        api_cls.return_value.get_messages.side_effect = requests.RequestException('fail')
        with mock.patch.object(configs, 'admin_user_ids', ['111']):
            handlers.fetch_messages(make_message(111))
        api_cls.return_value.send_message_to_group.assert_not_called()
        self.assertIn('Ошибка', bot_mock.reply_to.call_args[0][1])

from django.test import TestCase

# Create your tests here.
