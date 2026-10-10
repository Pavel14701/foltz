import os
from pathlib import Path
from datetime import timedelta

from common.config import env as conf
from common.utils import add_cache_control_headers

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = conf.DJANGO_SECRET

# SECURITY WARNING: don't run with debug turned on in production!
# Прод: DJANGO_DEBUG не задан или false. Для локальной разработки — DJANGO_DEBUG=True в .env
DEBUG = conf.DJANGO_DEBUG

ALLOWED_HOSTS = conf.DJANGO_ALLOWED_HOSTS
CSRF_TRUSTED_ORIGINS = conf.DJANGO_CSRF_TRUSTED_ORIGINS

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    'blog.apps.BlogConfig',
    'forms.apps.FormsConfig',
    'services.apps.ServicesConfig',
    'user.apps.UserConfig',
    'common.apps.CommonConfig',
    'products.apps.ProductsConfig',

    'rest_framework',
    'csp',
    'compressor',
]

# django-csp >= 4.0
CONTENT_SECURITY_POLICY = {
    'DIRECTIVES': {
        'default-src': ("'self'",),
        'img-src': ("'self'",),
        'media-src': ("'self'",),
        'script-src': ("'self'",),
        'style-src': ("'self'", 'https://fonts.googleapis.com'),
    }
}

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'csp.middleware.CSPMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
    'common.custom_error_middleware.CustomErrorMiddleware'
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Whitenoise ждёт функцию, а не строку-путь (иначе падает при старте)
WHITENOISE_ADD_HEADERS_FUNCTION = add_cache_control_headers
CLIENT_CACHE_MAX_AGE = conf.CLIENT_CACHE_MAX_AGE

ROOT_URLCONF = 'params.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'common.context_processors.site_contacts',
                'common.context_processors.request_form',
            ],
        },
    },
]

WSGI_APPLICATION = 'params.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': conf.POSTGRES_DB_NAME,
        'USER': conf.POSTGRES_DB_USER,
        'PASSWORD': conf.POSTGRES_DB_PASSWORD,
        'HOST': conf.POSTGRES_DB_HOST,
        'PORT': conf.POSTGRES_DB_PORT,
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS = {
    'host': conf.REDIS_HOST,
    'port': conf.REDIS_PORT,
    'db': conf.REDIS_DB_SESSION,
    #'password': 'your_redis_password',
    'socket_timeout': 1,
    'retry_on_timeout': False,
    #'unix_socket_path': None
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}



# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = conf.LANGUAGE_CODE
TIME_ZONE = conf.TIME_ZONE
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/' 
STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static'), ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{conf.REDIS_HOST}:{conf.REDIS_PORT}/{conf.REDIS_DB_CACHE}',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
CACHE_TTL = 60 * 60

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = conf.EMAIL_PORT
EMAIL_USE_TLS = conf.EMAIL_USE_TLS
EMAIL_HOST_USER = conf.EMAIL_SEND_FROM
EMAIL_HOST_PASSWORD = conf.EMAIL_HOST_PASSWORD

# Контактные данные сайта (используются во всех шаблонах через context processor)
SITE_PHONE = conf.SITE_PHONE
SITE_EMAIL = conf.SITE_EMAIL
SITE_ADDRESS = conf.SITE_ADDRESS
SITE_HOURS = conf.SITE_HOURS

# Яндекс-карта офиса («О нас»): JS API 2.1 (script + тайлы рендера + шрифты иконок).
CONTENT_SECURITY_POLICY['DIRECTIVES']['frame-src'] = ("'self'",)
CONTENT_SECURITY_POLICY['DIRECTIVES']['script-src'] = (
    "'self'", 'https://api-maps.yandex.ru', 'https://yastatic.net',
)
CONTENT_SECURITY_POLICY['DIRECTIVES']['img-src'] = (
    "'self'", 'data:',
    'https://core-stv.render.yandex.net',
    'https://core-renderer-tiles.maps.yandex.net',
    'https://yastatic.net',
)
CONTENT_SECURITY_POLICY['DIRECTIVES']['style-src'] = (
    # 'unsafe-inline' обязателен: JS API 2.1 расставляет inline-стили программно.
    "'self'", 'https://fonts.googleapis.com', 'https://yastatic.net', "'unsafe-inline'",
)
CONTENT_SECURITY_POLICY['DIRECTIVES']['font-src'] = ("'self'", 'https://yastatic.net', 'https://fonts.gstatic.com')
CONTENT_SECURITY_POLICY['DIRECTIVES']['connect-src'] = (
    "'self'", 'https://api-maps.yandex.ru', 'https://yandex.ru',
    'https://log.api-maps.yandex.ru',
)