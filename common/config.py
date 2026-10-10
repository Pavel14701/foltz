"""Типизированная конфигурация приложения: pydantic + os (без python-dotenv).

Переменные окружения читаются один раз при импорте и валидируются pydantic-моделью:
некорректная конфигурация падает на старте с понятной ошибкой, а не в рантайме.
Поддержка .env-файла реализована на чистом os: значения из .env не перезаписывают
уже установленные в системе переменные (setdefault), приоритет — у реального окружения.
"""
import os
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator

BASE_DIR = Path(__file__).resolve().parent.parent


def _load_dotenv(path: Path) -> None:
    """Минимальный загрузчик .env: KEY=VALUE, '#' — комментарии, кавычки снимаются."""
    if not path.is_file():
        return
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, _, value = line.partition('=')
        os.environ.setdefault(key.strip(), value.strip().strip('"\''))


def _split_csv(value: Any) -> Any:
    """'a, b, c' -> ['a', 'b', 'c'] (для списковых полей из переменных окружения)."""
    if isinstance(value, str):
        return [item.strip() for item in value.split(',') if item.strip()]
    return value


class Env(BaseModel):
    """Переменные окружения проекта: типы и дефолты задаются здесь, а не в settings."""

    model_config = ConfigDict(extra='ignore')

    # --- Django ---
    DJANGO_SECRET: str
    DJANGO_DEBUG: bool = False
    DJANGO_ALLOWED_HOSTS: list[str] = ['127.0.0.1', 'localhost']
    DJANGO_CSRF_TRUSTED_ORIGINS: list[str] = []

    # --- PostgreSQL ---
    POSTGRES_DB_NAME: str
    POSTGRES_DB_USER: str
    POSTGRES_DB_PASSWORD: str
    POSTGRES_DB_HOST: str = '127.0.0.1'
    POSTGRES_DB_PORT: int = 5432

    # --- Redis (сессии и кеш) ---
    REDIS_HOST: str = '127.0.0.1'
    REDIS_PORT: int = 6379
    REDIS_DB_SESSION: int = 1
    REDIS_DB_CACHE: int = 2

    # --- Прочее ---
    LANGUAGE_CODE: str = 'ru'
    TIME_ZONE: str = 'Europe/Minsk'
    CLIENT_CACHE_MAX_AGE: int = 86400

    # --- Почта (SMTP) ---
    EMAIL_PORT: int = 587
    EMAIL_USE_TLS: bool = True
    EMAIL_SEND_FROM: str = ''
    EMAIL_HOST_PASSWORD: str = ''

    # --- Контакты сайта (шапка/футер/CTA) ---
    SITE_PHONE: str = '+375 (44) 577-00-04'
    SITE_EMAIL: str = 'volksagro@gmail.com'
    SITE_ADDRESS: str = 'г. Минск, ул. Сухаревская, д. 16, пом. 6'
    SITE_HOURS: str = 'Пн–Пт: 09:00–17:00'

    # --- Статик API Яндекс.Карт (карта офиса на «О нас», без рекламы) ---
    YANDEX_MAPS_API_KEY: str = ''

    # --- Сайт и Telegram-бот ---
    SITE_BASE_URL: str = ''
    SITE_API_URL: str = ''

    # --- Telegram-бот (заявки) ---
    BOT_TOKEN: str = ''
    CHAT_ID: str = ''

    # --- Формы (почта) и Telegram-бот ---
    SEND_TO_EMAIL: list[str] = []
    SEND_FROM_EMAIL: str = ''
    SUPERGROUP_ID: str = ''
    ADMIN_IDS: list[str] = []
    NOTIFY_USER_IDS: list[str] = []
    YOUR_SITE_API_URL: str = ''
    USE_WEBHOOK: bool = False
    BOT_WEBHOOK: str = ''
    SITE_ADMIN_NAME: str = ''
    SITE_ADMIN_PASSWORD: str = ''

    @field_validator('DJANGO_ALLOWED_HOSTS', 'DJANGO_CSRF_TRUSTED_ORIGINS',
                     'SEND_TO_EMAIL', 'ADMIN_IDS', 'NOTIFY_USER_IDS', mode='before')
    @classmethod
    def _csv_to_list(cls, value: Any) -> Any:
        return _split_csv(value)


_load_dotenv(BASE_DIR / '.env')

env = Env(**{
    key: value
    for key, value in os.environ.items()
    if key in Env.model_fields
})
