"""DTO с конфигурацией для форм обратной связи и Telegram-бота.

Значения берутся из валидированного окружения `common.config.env`.
"""
from dataclasses import dataclass, field
from typing import List

from common.config import env


@dataclass
class FormData:
    name: str
    phone: str
    question: str
    send_to_email: List[str] = field(init=False)
    send_from_email: str = field(init=False)
    bot_token: str = field(init=False)
    chat_id: str = field(init=False)

    def __post_init__(self):
        self.send_to_email = env.SEND_TO_EMAIL
        self.send_from_email = env.SEND_FROM_EMAIL
        self.bot_token = env.BOT_TOKEN
        self.chat_id = env.CHAT_ID


@dataclass
class DtoBotConfigs:
    supergroup_id: str = field(init=False)
    admin_user_ids: List[str] = field(init=False)
    notify_user_ids: List[str] = field(init=False)
    bot_token: str = field(init=False)
    site_api_url: str = field(init=False)
    use_webhook: bool = field(init=False)
    bot_webhook: str = field(init=False)
    username: str = field(init=False)
    password: str = field(init=False)

    def __post_init__(self):
        self.supergroup_id = env.SUPERGROUP_ID
        self.admin_user_ids = env.ADMIN_IDS
        self.notify_user_ids = env.NOTIFY_USER_IDS
        self.bot_token = env.BOT_TOKEN
        self.site_api_url = env.YOUR_SITE_API_URL
        self.use_webhook = env.USE_WEBHOOK
        self.bot_webhook = env.BOT_WEBHOOK
        self.username = env.SITE_ADMIN_NAME
        self.password = env.SITE_ADMIN_PASSWORD

    def notification_targets(self) -> List[str]:
        """Получатели заявки: супергруппа + круг пользователей.

        Круг пользователей берётся из NOTIFY_USER_IDS, а если он не задан —
        из ADMIN_IDS. Дубликаты и пустые значения отбрасываются.
        """
        recipients = [self.supergroup_id, *(self.notify_user_ids or self.admin_user_ids)]
        seen: set = set()
        unique = []
        for chat_id in recipients:
            chat_id = str(chat_id).strip()
            if chat_id and chat_id not in seen:
                seen.add(chat_id)
                unique.append(chat_id)
        return unique
