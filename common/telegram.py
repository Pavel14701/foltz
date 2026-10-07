"""Отправка заявок в Telegram: в группу и выбранному кругу пользователей.

Используется формой на сайте (`common.aplications`). Сам бот
(`bot.handlers`) шлёт через свой инстанс telebot, но список получателей
у обоих путей один — `NOTIFY_USER_IDS` (или `ADMIN_IDS`).
"""
import logging

import requests

from common.config import env

logger = logging.getLogger(__name__)

_API_URL = 'https://api.telegram.org/bot{token}/sendMessage'
_TIMEOUT = 10  # секунд на запрос к Telegram API


def notification_recipients() -> list:
    """Список получателей заявки: группа + круг пользователей.

    Круг пользователей берётся из NOTIFY_USER_IDS; если он не задан —
    из ADMIN_IDS. Дубликаты и пустые значения отбрасываются.
    """
    recipients = [env.CHAT_ID, *(env.NOTIFY_USER_IDS or env.ADMIN_IDS)]
    seen: set = set()
    unique = []
    for chat_id in recipients:
        chat_id = str(chat_id).strip()
        if chat_id and chat_id not in seen:
            seen.add(chat_id)
            unique.append(chat_id)
    return unique


def send_telegram_message(text: str, chat_ids: list | None = None) -> list:
    """Шлёт `text` каждому получателю через Bot API.

    Возвращает список chat_id, которым доставить не удалось.
    Ошибка одного получателя не прерывает рассылку остальным.
    """
    token = env.BOT_TOKEN.strip()
    if not token:
        logger.warning('BOT_TOKEN не задан — сообщение в Telegram не отправлено')
        return []

    failed = []
    for chat_id in (chat_ids if chat_ids is not None else notification_recipients()):
        try:
            response = requests.post(
                _API_URL.format(token=token),
                data={'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'},
                timeout=_TIMEOUT,
            )
            if not response.ok:
                logger.error('Telegram отклонил сообщение для %s: %s', chat_id, response.text)
                failed.append(chat_id)
        except requests.RequestException as exc:
            logger.error('Не удалось отправить сообщение пользователю %s: %s', chat_id, exc)
            failed.append(chat_id)
    return failed
