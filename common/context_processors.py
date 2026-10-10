import re

from django.conf import settings
from django.http import HttpRequest

from common.config import env
from forms.forms import ContactForm


def site_contacts(request: HttpRequest) -> dict:
    """Контактные данные сайта — единый источник для всех шаблонов (DRY)."""
    return {
        'site': {
            'phone': settings.SITE_PHONE,
            'phone_link': re.sub(r'[^\d+]', '', settings.SITE_PHONE),
            'email': settings.SITE_EMAIL,
            'address': settings.SITE_ADDRESS,
            'hours': settings.SITE_HOURS,
            # JS API Яндекс.Карт на «О нас»; пусто -> статичная картинка-фолбэк.
            'yandex_maps_api_key': env.YANDEX_MAPS_API_KEY,
        }
    }


def request_form(request: HttpRequest) -> dict:
    """Форма заявки на каждой странице (партиал forms/_request_form.html)."""
    return {'contact_form': ContactForm()}