"""Тесты конфигурации, DTO, Telegram-отправителя и рассылки заявок."""
import requests
from unittest import mock

from django.test import SimpleTestCase

from common import dto as dto_module
from common import telegram as telegram_module
from common.aplications import SendAplications
from common.config import Env
from common.dto import DtoBotConfigs, FormData
from common.telegram import notification_recipients, send_telegram_message


def env_kwargs(**extra):
    """Минимальный набор для конструирования Env (обязательные поля)."""
    kwargs = {
        'DJANGO_SECRET': 'test-secret',
        'POSTGRES_DB_NAME': 'db',
        'POSTGRES_DB_USER': 'user',
        'POSTGRES_DB_PASSWORD': 'pass',
    }
    kwargs.update(extra)
    return kwargs


class EnvModelTest(SimpleTestCase):
    def test_missing_required_fails(self):
        with self.assertRaises(Exception):
            Env(DJANGO_SECRET='only-secret')

    def test_csv_lists_parsed(self):
        conf = Env(**env_kwargs(
            DJANGO_ALLOWED_HOSTS='a.com, b.com ,,c.com',
            NOTIFY_USER_IDS='1,2',
        ))
        self.assertEqual(conf.DJANGO_ALLOWED_HOSTS, ['a.com', 'b.com', 'c.com'])
        self.assertEqual(conf.NOTIFY_USER_IDS, ['1', '2'])

    def test_bool_and_int_coercion(self):
        conf = Env(**env_kwargs(
            DJANGO_DEBUG='True',
            USE_WEBHOOK='1',
            EMAIL_PORT='2525',
            POSTGRES_DB_PORT='6543',
        ))
        self.assertTrue(conf.DJANGO_DEBUG)
        self.assertTrue(conf.USE_WEBHOOK)
        self.assertEqual(conf.EMAIL_PORT, 2525)
        self.assertEqual(conf.POSTGRES_DB_PORT, 6543)

    def test_defaults(self):
        conf = Env(**env_kwargs())
        self.assertFalse(conf.DJANGO_DEBUG)
        self.assertEqual(conf.SEND_TO_EMAIL, [])
        self.assertEqual(conf.ADMIN_IDS, [])
        self.assertEqual(conf.NOTIFY_USER_IDS, [])
        self.assertFalse(conf.USE_WEBHOOK)


class NotificationRecipientsTest(SimpleTestCase):
    @mock.patch.object(telegram_module.env, 'NOTIFY_USER_IDS', ['555', '666'])
    @mock.patch.object(telegram_module.env, 'ADMIN_IDS', ['111', '222'])
    @mock.patch.object(telegram_module.env, 'CHAT_ID', '-100')
    def test_group_plus_notify_users(self):
        self.assertEqual(notification_recipients(), ['-100', '555', '666'])

    @mock.patch.object(telegram_module.env, 'NOTIFY_USER_IDS', [])
    @mock.patch.object(telegram_module.env, 'ADMIN_IDS', ['111', '222'])
    @mock.patch.object(telegram_module.env, 'CHAT_ID', '-100')
    def test_fallback_to_admin_ids(self):
        self.assertEqual(notification_recipients(), ['-100', '111', '222'])

    @mock.patch.object(telegram_module.env, 'NOTIFY_USER_IDS', ['111', '', '111'])
    @mock.patch.object(telegram_module.env, 'ADMIN_IDS', [])
    @mock.patch.object(telegram_module.env, 'CHAT_ID', '-100')
    def test_dedup_and_empty_skipped(self):
        self.assertEqual(notification_recipients(), ['-100', '111'])


class SendTelegramMessageTest(SimpleTestCase):
    @mock.patch.object(telegram_module.env, 'BOT_TOKEN', '')
    @mock.patch('common.telegram.requests.post')
    def test_no_token_no_requests(self, post_mock):
        self.assertEqual(send_telegram_message('text', ['a']), [])
        post_mock.assert_not_called()

    @mock.patch.object(telegram_module.env, 'BOT_TOKEN', '123:test')
    @mock.patch('common.telegram.requests.post')
    def test_sends_to_each_recipient(self, post_mock):
        post_mock.return_value = mock.Mock(ok=True)
        self.assertEqual(send_telegram_message('text', ['a', 'b']), [])
        self.assertEqual(post_mock.call_count, 2)
        _, kwargs = post_mock.call_args
        self.assertEqual(kwargs['data']['parse_mode'], 'HTML')
        self.assertEqual(kwargs['timeout'], 10)

    @mock.patch.object(telegram_module.env, 'BOT_TOKEN', '123:test')
    @mock.patch('common.telegram.requests.post')
    def test_http_error_reported(self, post_mock):
        post_mock.return_value = mock.Mock(ok=False, text='chat not found')
        self.assertEqual(send_telegram_message('text', ['bad']), ['bad'])

    @mock.patch.object(telegram_module.env, 'BOT_TOKEN', '123:test')
    @mock.patch('common.telegram.requests.post')
    def test_network_error_reported(self, post_mock):
        post_mock.side_effect = requests.RequestException('boom')
        self.assertEqual(send_telegram_message('text', ['bad']), ['bad'])


class DtoBotConfigsTest(SimpleTestCase):
    def test_targets_group_plus_notify(self):
        c = DtoBotConfigs()
        c.supergroup_id = '-grp'
        c.admin_user_ids = ['111', '222']
        c.notify_user_ids = ['333', '111', '']
        self.assertEqual(c.notification_targets(), ['-grp', '333', '111'])

    def test_targets_fallback_to_admins(self):
        c = DtoBotConfigs()
        c.supergroup_id = '-grp'
        c.admin_user_ids = ['111', '222']
        c.notify_user_ids = []
        self.assertEqual(c.notification_targets(), ['-grp', '111', '222'])


class FormDataTest(SimpleTestCase):
    @mock.patch.object(dto_module.env, 'SEND_TO_EMAIL', ['a@b.ru', 'c@d.ru'])
    @mock.patch.object(dto_module.env, 'SEND_FROM_EMAIL', 'from@x.ru')
    @mock.patch.object(dto_module.env, 'BOT_TOKEN', 'tok')
    @mock.patch.object(dto_module.env, 'CHAT_ID', '-chat')
    def test_form_data_reads_env(self):
        data = FormData('Иван', '+375291112233', 'Вопрос')
        self.assertEqual(data.send_to_email, ['a@b.ru', 'c@d.ru'])
        self.assertEqual(data.send_from_email, 'from@x.ru')
        self.assertEqual(data.bot_token, 'tok')
        self.assertEqual(data.chat_id, '-chat')


class SendAplicationsTest(SimpleTestCase):
    @mock.patch.object(dto_module.env, 'SEND_TO_EMAIL', ['a@b.ru'])
    @mock.patch.object(dto_module.env, 'SEND_FROM_EMAIL', 'from@x.ru')
    @mock.patch.object(dto_module.env, 'BOT_TOKEN', 'tok')
    @mock.patch.object(dto_module.env, 'CHAT_ID', '-chat')
    @mock.patch('common.aplications.send_mail')
    def test_email_recipients_not_nested(self, send_mail_mock):
        SendAplications(FormData('Иван', '123', '?')).email()
        args, kwargs = send_mail_mock.call_args
        self.assertEqual(args[0], 'Новая заявка')
        self.assertIn('Имя: Иван', args[1])
        self.assertEqual(args[2], 'from@x.ru')
        self.assertEqual(args[3], ['a@b.ru'])  # не [ ['a@b.ru'] ]
        self.assertFalse(kwargs['fail_silently'])

    @mock.patch('common.aplications.send_telegram_message')
    def test_tg_escapes_user_input(self, send_mock):
        send_mock.return_value = []
        SendAplications(FormData('<b>Иван</b>', '123', '?')).tg()
        text = send_mock.call_args[0][0]
        self.assertIn('Новая заявка', text)
        self.assertIn('&lt;b&gt;Иван&lt;/b&gt;', text)

    @mock.patch('common.aplications.send_telegram_message')
    def test_tg_logs_failed_recipients(self, send_mock):
        send_mock.return_value = ['123']
        with self.assertLogs('common.aplications', level='WARNING') as logs:
            SendAplications(FormData('Иван', '123', '?')).tg()
        self.assertIn('123', logs.output[0])
