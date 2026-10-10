import re

from django.conf import settings
from django.http import HttpRequest

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
        }
    }


def request_form(request: HttpRequest) -> dict:
    """Форма заявки на каждой странице (партиал forms/_request_form.html)."""
    return {'contact_form': ContactForm()}