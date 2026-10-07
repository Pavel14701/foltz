"""Smoke-тест: рендеринг всех страниц и валидность сид-данных (без обращения к БД).

Запуск: uv run python smoke_test.py
"""
import os
from datetime import datetime
from types import SimpleNamespace

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'params.settings')
django.setup()

from django.template.loader import render_to_string  # noqa: E402
from django.test import RequestFactory  # noqa: E402
from django.urls import reverse  # noqa: E402

from blog.seed_data import POSTS  # noqa: E402
from forms.forms import ContactForm  # noqa: E402
from services.seed_data import SERVICES  # noqa: E402

request = RequestFactory().get('/')


def check(name: str, template: str, context: dict) -> None:
    html = render_to_string(template, context, request=request)
    assert '<html' in html.lower(), f'{name}: нет <html>'
    assert 'Фольц' in html, f'{name}: нет бренда'
    print(f'OK  {name} ({len(html)} bytes)')


# --- Главная и статические страницы ---
check('home', 'home.html', {})
check('about', 'about.html', {})
check('contact', 'forms/contact.html', {'form': ContactForm()})

# --- Каталог и страница услуги (моки вместо объектов БД) ---
service_mocks = [
    SimpleNamespace(slug=s['slug'], title=s['title'], preview_text=s['preview_text'], preview_image=None)
    for s in SERVICES
]
check('services list', 'services/service_list.html', {'services': service_mocks})

service_mock = SimpleNamespace(
    slug=SERVICES[0]['slug'],
    title=SERVICES[0]['title'],
    preview_image=None,
    preview_video_url='',
    service_section=[],
)
check('service detail', 'services/service_detail.html', {'service': service_mock})

# --- Блог ---
check('post list (empty)', 'blog/post_list.html', {'posts': []})

post_mock = SimpleNamespace(
    slug=POSTS[0]['slug'],
    title=POSTS[0]['title'],
    preview_image=None,
    preview_video_url='',
    created_at=datetime(2026, 1, 15),
    blog_section=[
        SimpleNamespace(order=s['order'], subtitle=s.get('subtitle', ''),
                        content=s.get('content', ''), image=None, youtube_url='')
        for s in POSTS[0]['sections']
    ],
)
check('post list', 'blog/post_list.html', {'posts': [post_mock]})
check('post detail', 'blog/post_details.html', {'post': post_mock})

# --- URL-ы сид-данных разрешаются ---
for s in SERVICES:
    reverse('services:service_detail', args=[s['slug']])
for p in POSTS:
    reverse('blog:post_detail', args=[p['slug']])
print(f'OK  urls: {len(SERVICES)} услуг, {len(POSTS)} статей')

# --- Валидность секций (ровно одно поле, как требует clean()) ---
for p in POSTS:
    for s in p['sections']:
        filled = [f for f in ('subtitle', 'content', 'youtube_url') if s.get(f)]
        assert len(filled) == 1, f"{p['slug']} order={s['order']}: поля {filled}"
print('OK  seed sections: по одному полю на секцию')

print('\nSMOKE OK')
