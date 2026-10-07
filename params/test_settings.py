"""Настройки для тестового прогона: manage.py test --settings=params.test_settings.

SQLite в памяти вместо PostgreSQL и упрощённое хранилище статики —
тесты идут на любой машине без внешних сервисов (Postgres/Redis/сеть).
"""
from params.settings import *  # noqa: F401,F403

import os  # noqa: E402

ALLOWED_HOSTS = list(dict.fromkeys([*ALLOWED_HOSTS, 'testserver', 'localhost', '127.0.0.1']))

# По умолчанию — SQLite в памяти (тесты).
# Для запуска дев-сервера на тестовых настройках задайте TEST_DB_FILE:
#   TEST_DB_FILE=db.test.sqlite3 python manage.py migrate --settings=params.test_settings
_test_db_file = os.environ.get('TEST_DB_FILE')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': _test_db_file or ':memory:',
    }
}

# Без манифеста whitenoise: не требуем collectstatic при тестах
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Письма не уходят по SMTP
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
