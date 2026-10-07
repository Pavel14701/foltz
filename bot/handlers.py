import logging

import requests
from telebot.apihelper import ApiTelegramException
from telebot.types import Message

from bot.bot_instance import bot, configs

logger = logging.getLogger(__name__)

_TIMEOUT = 10  # секунд на запрос к API сайта


class SiteMsgAPI:
    api_url = configs.site_api_url

    def get_messages(self):
        response = requests.get(self.api_url, timeout=_TIMEOUT)
        response.raise_for_status()
        return response.json()

    def send_message_to_site(self, sender, body):
        data = {
            'sender': sender,
            'body': body,
        }
        response = requests.post(self.api_url, json=data, timeout=_TIMEOUT)
        response.raise_for_status()
        return response.json()

    def send_message_to_group(self, sender, subject, body):
        """Заявка уходит в супергруппу и каждому из круга пользователей.

        Сбой доставки одному получателю не прерывает рассылку остальным.
        """
        message = f'Сообщение от {sender}:\nТема: {subject}\n{body}'
        for chat_id in configs.notification_targets():
            try:
                bot.send_message(chat_id, message)
            except ApiTelegramException:
                logger.exception('Не удалось доставить заявку получателю %s', chat_id)


def send_welcome(message: Message):
    if str(message.from_user.id) in configs.admin_user_ids:
        return bot.reply_to(
            message,
            'Вы администратор. Команда "/messages" — получить заявки с сайта.',
        )
    bot.reply_to(
        message,
        'Здравствуйте! Это служебный бот сайта «Фольц». '
        'Оставить заявку можно на сайте в разделе «Контакты».',
    )


def fetch_messages(message: Message):
    """Раздаёт заявки с сайта: в группу и кругу пользователей."""
    if str(message.from_user.id) not in configs.admin_user_ids:
        return
    api = SiteMsgAPI()
    try:
        messages = api.get_messages()
    except (requests.RequestException, ValueError):
        logger.exception('Не удалось получить заявки с сайта')
        return bot.reply_to(message, 'Ошибка: не удалось получить заявки с сайта.')
    for msg in messages:
        api.send_message_to_group(msg['name'], msg['subject'], msg['body'])
    bot.reply_to(message, f'Разослано заявок: {len(messages)}.')


def handle_group_messages(message: Message):
    api = SiteMsgAPI()
    if message.reply_to_message and str(message.chat.id) in configs.admin_user_ids:
        original_message = message.reply_to_message.text
        # Предполагается, что оригинальное сообщение имеет формат:
        # "Сообщение от {sender}:\nТема: {subject}\n{body}"
        sender_info, subject_info, body_info = original_message.split('\n', 2)
        sender = sender_info.replace('Сообщение от ', '').strip()
        response_body = message.text
        api.send_message_to_site(sender, response_body)
        bot.reply_to(message, 'Ответ отправлен на сайт!')
