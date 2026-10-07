import re

from django.conf import settings
from django.http import HttpRequest


def site_contacts(request: HttpRequest) -> dict:
    """Контактные данные сайта — единый источник для всех шаблонов (DRY)."""
    return {
        'site': {
            'phone': settings.SITE_PHONE,
            'phone_link': re.sub(r'[^\d+]', '', settings.SITE_PHONE),
            'email': settings.SITE_EMAIL,
            'address': settings.SITE_ADDRESS,
        }
    }