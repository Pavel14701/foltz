# Фольц — сайт агросервиса

Сайт компании по ремонту гидравлики, двигателей и спецтехники (Django 5.2).

## Запуск (разработка)

1. Создать окружение и установить зависимости: `uv sync`
2. Скопировать `.env.example` в `.env` и заполнить значения: `cp .env.example .env`
3. Применить миграции и наполнить данные: `python manage.py migrate && python manage.py seed_services && python manage.py seed_posts && python manage.py seed_products`
4. Запуск: `python manage.py runserver`

## Конфигурация

Все настройки окружения читаются один раз при старте и валидируются pydantic-моделью
`Env` (см. `common/config.py`). Поддерживается файл `.env`; приоритет — у переменных
реального окружения. Список переменных и значения по умолчанию — в `common/config.py`
и `.env.example`.

## Тесты

Встроенный раннер Django, без внешних сервисов (SQLite в памяти, локальный
почтовый бэкенд): `python manage.py test --settings=params.test_settings`

Покрытие: конфигурация `Env` и `common/telegram.py`, DTO и рассылка заявок
(`common/aplications.py`), обработчики Telegram-бота (`bot/handlers.py`),
форма обратной связи (`forms`), модели и страницы блога, seed-команда и
sitemap (`blog`), услуги и товары (`services`, `products`).

Дополнительно `python smoke_test.py` — быстрая проверка рендера страниц без БД.

## Стек

Django 5.2, DRF + SimpleJWT, PostgreSQL (psycopg 3), Redis (сессии и кеш),
Bootstrap 5.3 (вендорится локально в `static/vendor/`), WhiteNoise, django-csp 4.x,
pytils (ЧПУ-slug).

[project.dependencies]
django = ">=5.2"
django-redis = ">=6.0.0"
django-redis-sessions = ">=0.6.2"
django-csp = ">=4.0"
django-compressor = ">=4.5.1"
djangorestframework = ">=3.16.0"
djangorestframework-simplejwt = ">=5.4.0"
psycopg = { version = ">=3.2.9", extras = ["binary"] }
pillow = ">=11.3.0"
pydantic = ">=2.11.7"
pytils = ">=0.4.4"
pytelegrambotapi = ">=4.28.0"
redis = ">=6.2.0"
requests = ">=2.32.4"
whitenoise = ">=6.9.0"
gunicorn = ">=23.0.0"


[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
