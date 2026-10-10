"""Генерация статичной карты офиса для страницы «О нас» (static/images/about-map.jpg).

Если в .env задан YANDEX_MAPS_API_KEY (бесплатный ключ Статик API Яндекс.Карт) —
карта скачивается из Яндекса: без рекламных плашек, с фирменным красным маркером.
Иначе фрагмент района склеивается из тайлов OpenStreetMap (тоже без рекламы,
но со своей отрисовкой маркера). Атрибуция источника — в шаблоне.

Запуск: python manage.py make_map
"""
import io
import json
import math
import urllib.request
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from PIL import Image, ImageDraw

from common.config import BASE_DIR, env

LAT, LON, ZOOM = 53.8859313, 27.4388081, 16  # ул. Сухаревская, 16 — офис
OUT_PATH = Path(BASE_DIR) / 'static' / 'images' / 'about-map.jpg'
_UA = 'foltz-site-map/1.0 (contact: volksagro@gmail.com)'


def _fetch(url: str) -> bytes:
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', _UA)]
    with opener.open(url, timeout=30) as response:
        return response.read()


def _from_yandex_v1(api_key: str) -> Image.Image:
    """Статик API v1 (по ключу): 650x450 — максимальный размер без Enterprise."""
    params = (
        f'apikey={api_key}'
        f'&ll={LON},{LAT}&z={ZOOM}&l=map&size=650,450'
        f'&pt={LON},{LAT},pm2rdm'  # красный маркер
    )
    return Image.open(io.BytesIO(_fetch(f'https://static-maps.yandex.ru/v1?{params}'))).convert('RGB')


def _from_yandex_1x() -> Image.Image:
    """Легаси-endpoint 1.x: работает без ключа, та же отрисовка Яндекса."""
    params = f'll={LON},{LAT}&z={ZOOM}&l=map&size=650,450&pt={LON},{LAT},pm2rdm'
    return Image.open(io.BytesIO(_fetch(f'https://static-maps.yandex.ru/1.x/?{params}'))).convert('RGB')


def _from_osm() -> Image.Image:
    """Склейка тайлов OpenStreetMap 3x2 (zoom 16) + свой маркер."""
    def deg2tile(lat: float, lon: float, z: int) -> tuple[int, int]:
        n = 2 ** z
        x = int((lon + 180) / 360 * n)
        y = int((1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n)
        return x, y

    xt, yt = deg2tile(LAT, LON, ZOOM)
    cols, rows = 3, 2
    canvas = Image.new('RGB', (cols * 256, rows * 256))
    for dy in range(rows):
        for dx in range(cols):
            url = f'https://tile.openstreetmap.org/{ZOOM}/{xt + dx}/{yt + dy}.png'
            tile = Image.open(io.BytesIO(_fetch(url))).convert('RGB')
            canvas.paste(tile, (dx * 256, dy * 256))

    # Позиция офиса на канве.
    fx = ((LON + 180) / 360 * 2 ** ZOOM - xt) * 256
    fy = ((1 - math.log(math.tan(math.radians(LAT)) + 1 / math.cos(math.radians(LAT))) / math.pi)
          / 2 * 2 ** ZOOM - yt) * 256
    draw = ImageDraw.Draw(canvas)
    r = 12
    draw.polygon([(fx, fy), (fx - 9, fy - 26), (fx + 9, fy - 26)], fill=(178, 34, 34))
    draw.ellipse([fx - r, fy - 26 - r, fx + r, fy - 26 + r], fill=(178, 34, 34),
                 outline=(120, 10, 10), width=2)
    draw.ellipse([fx - 4, fy - 30, fx + 4, fy - 22], fill=(255, 255, 255))
    return canvas


class Command(BaseCommand):
    help = 'Генерирует static/images/about-map.jpg (Яндекс Статик API по ключу, иначе OSM-тайлы).'

    def handle(self, *args, **options) -> None:
        api_key = env.YANDEX_MAPS_API_KEY
        source = 'Яндекс.Карты'
        image = None
        if api_key:
            try:
                image = _from_yandex_v1(api_key)
            except Exception as exc:  # noqa: BLE001
                self.stdout.write(self.style.WARNING(
                    f'Статик API v1 недоступен ({exc}), пробую легаси 1.x.'))
        if image is None:
            try:
                image = _from_yandex_1x()
            except Exception as exc:  # noqa: BLE001
                self.stdout.write(self.style.WARNING(
                    f'1.x недоступен ({exc}), склеиваю из тайлов OSM.'))
                source = 'OpenStreetMap'
        if image is None:
            image = _from_osm()

        OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        image.save(OUT_PATH, quality=88)
        # Атрибуция на странице подбирается по источнику (см. site_contacts).
        source_slug = 'yandex' if (api_key and source.startswith('Яндекс')) else 'osm'
        OUT_PATH.with_suffix('.json').write_text(
            json.dumps({'source': source_slug}), encoding='utf-8')
        self.stdout.write(self.style.SUCCESS(
            f'OK: {OUT_PATH.relative_to(BASE_DIR)} ({image.size[0]}x{image.size[1]}), источник: {source}.'))