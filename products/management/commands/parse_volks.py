"""Парсер каталога volks.by: товары по категориям + прайсы услуг.

Тянет https://volks.by/tovary/ (таблицы «категория → наименование/цена»)
и https://volks.by/uslugi/ (таблицы «группа работ → наименование/ед./цена»).
Идемпотентно: update_or_create по названию.

Запуск: uv run python manage.py parse_volks [--no-services] [--no-products]
"""

import re
import urllib.request

from django.core.management.base import BaseCommand
from django.db import transaction

from products.models import Product, ProductCategory
from services.models import Service, ServicePrice

BASE_URL = 'https://volks.by'

# Категории товаров: ключ — подстрока заголовка h2 на доноре.
CATEGORY_RULES = [
    ('Амкодор', {
        'title': 'Запчасти для техники Амкодор',
        'order': 10,
        'repair_slug': 'remont-tehniki-amkodor',
        'cta_title': 'Нужен ремонт Амкодор?',
        'cta_text': 'Отремонтируем узел на своём стенде или подберём готовый из обменного фонда. '
                    'Позвоните — согласуем цену и срок.',
    }),
    ('МТЗ', {
        'title': 'Запчасти для техники МТЗ',
        'order': 20,
        'repair_slug': 'remont-traktorov-mtz',
        'cta_title': 'Нужен ремонт трактора МТЗ?',
        'cta_text': 'Капитальный ремонт энергонасыщенных МТЗ 2822, 3022, 3522: от дефектовки '
                    'до сборки и обкатки. Позвоните — рассчитаем стоимость.',
    }),
    ('гидравл', {
        'title': 'Запчасти для гидравлических систем',
        'order': 30,
        'repair_slug': 'remont-gidronasosov',
        'cta_title': 'Нужен ремонт гидравлики?',
        'cta_text': 'Ремонтируем гидронасосы, гидромоторы, цилиндры и распределители с проверкой '
                    'на стенде и гарантией. Позвоните — подскажем по вашему узлу.',
    }),
    ('Метизы', {
        'title': 'Метизы',
        'order': 40,
        'repair_slug': '',
        'cta_title': 'Не нашли нужную запчасть?',
        'cta_text': 'Каталог обновляется — позвоните, уточним наличие и подберём аналог '
                    'под вашу технику.',
    }),
    # Категория «Обменный фонд (восстановленные узлы)» создаётся seed_products.
]

# Группы прайса услуг: ключ — подстрока заголовка h2 на доноре.
SERVICE_RULES = [
    ('гидравлики мтз', 'remont-gidravliki-mtz'),
    ('гидравлик', 'remont-gidrotransmissiy'),
    ('импортной сельскохозяйственной', 'remont-importnoy-tehniki'),
    ('двигателей', 'kapremont-dvigateley'),
    ('диагностика', 'vyezdnaya-diagnostika-gidrosistem'),
    ('тракторов', 'remont-traktorov-mtz'),
    ('амкодор', 'remont-tehniki-amkodor'),
]

# Маппинг строк прайса донора на конкретные услуги: каждый узел — своя
# карточка со своей ценой (а не общие группы «вперемешку»).
ROW_RULES = [
    ('диагностика гмп', 'diagnostika-gmp-amkodor'),
    ('диагностика гидротормоз', 'diagnostika-gidrotormozov'),
    ('диагностика рулев', 'diagnostika-rulevogo-upravleniya'),
    ('диагностика погрузочного', 'diagnostika-pogruzochnogo-oborudovaniya'),
    ('диагностика гидрораспределителя', 'diagnostika-gidroraspredelitelya-mtz'),
    ('диагностика', 'vyezdnaya-diagnostika-gidrosistem'),
    ('выезд специалиста', 'vyezdnaya-diagnostika-gidrosistem'),
    ('гмп', 'remont-gmp-amkodor'),
    ('главной передачи', 'remont-glavnoy-peredachi-amkodor'),
    ('гидротормоза', 'remont-gidrotormoza-amkodor'),
    ('сочленения', 'remont-sochleneniya-amkodor'),
    ('балансира', 'remont-balansira-amkodor'),
    ('рома', 'remont-roma-amkodor'),
    ('погрузочного оборудования', 'remont-pogruzochnogo-oborudovaniya'),
    ('мостов', 'remont-mostov-amkodor'),
    ('двигателя', 'kapremont-dvigateley'),
    ('двигателей', 'kapremont-dvigateley'),
    ('zms', 'remont-gidravliki-mtz'),
    ('рп-70', 'remont-gidravliki-mtz'),
    ('a10cn045', 'remont-gidravliki-mtz'),
    ('гидронасос', 'remont-gidronasosov'),
    ('гидромотор', 'remont-gidromotorov'),
    ('гидроцилиндр', 'remont-gidrocilindrov'),
    ('гидрораспределитель', 'remont-gidroraspredeliteley'),
    ('гидростатических трансмиссий', 'remont-gidrotransmissiy'),
    ('демонтаж', None),  # None → берём услугу по заголовку таблицы
    ('монтаж', None),
    ('разборка', None),
    ('сборка', None),
    ('крепёж', None),
    ('крепеж', None),
    ('регулиров', None),
    ('проверка', None),
]

# Точечные правки опечаток и сокращений донора.
TITLE_FIXES = {
    'воссстановленная': 'восстановленная',
}


def fetch_html(url: str) -> str:
    """Скачивает страницу (кодировка utf-8, у старых страниц — cp1251)."""
    request = urllib.request.Request(
        url, headers={'User-Agent': 'Mozilla/5.0 (compatible; FoltzParser/1.0)'},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        raw = response.read()
    for encoding in ('utf-8', 'cp1251'):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode('utf-8', errors='replace')


def strip_tags(fragment: str) -> str:
    text = re.sub(r'<[^>]+>', '', fragment)
    return text.replace('&nbsp;', ' ').replace('&amp;', '&').strip()


def normalize_price(raw: str) -> str:
    """«9750р.» → «9 750 р.», «1900р./2300р.» → «1900/2300 р.», «договорная» → как есть."""
    text = strip_tags(raw).strip(' .')
    if not text:
        return ''
    if 'договор' in text.lower():
        return 'договорная'
    text = text.replace('р.', '').replace('р', '').replace('руб', '').strip(' .,/')
    numbers = [n.strip() for n in text.split('/') if n.strip().isdigit()]
    if not numbers:
        return ''
    pretty = [f'{int(n):,}'.replace(',', ' ') for n in numbers]
    return f"{'/'.join(pretty)} р."


def parse_tables(html: str):
    """Возвращает [(заголовок h2, [(ячейки строки…), …]), …] в порядке следования."""
    result = []
    current_heading = None
    for part in re.split(r'(<h2[^>]*>.*?</h2>|<table.*?</table>)', html, flags=re.S):
        if part.startswith('<h2'):
            current_heading = strip_tags(part)
        elif part.startswith('<table'):
            rows = []
            for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', part, re.S):
                cells = [strip_tags(td) for td in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', tr, re.S)]
                if any(cells):
                    rows.append(cells)
            result.append((current_heading, rows))
    return result


class Command(BaseCommand):
    help = 'Парсит товары и прайсы услуг с volks.by (идемпотентно).'

    def add_arguments(self, parser):
        parser.add_argument('--no-products', action='store_true', help='Не обновлять товары.')
        parser.add_argument('--no-services', action='store_true', help='Не обновлять прайсы услуг.')

    def handle(self, *args, **options) -> None:
        if not options['no_products']:
            self.parse_products()
        if not options['no_services']:
            self.parse_services()

    # ---- Товары -------------------------------------------------------

    def parse_products(self) -> None:
        html = fetch_html(f'{BASE_URL}/tovary/')
        categories = self.ensure_categories()
        created_count = 0
        updated_count = 0
        with transaction.atomic():
            for heading, rows in parse_tables(html):
                category = self.match_category(heading, categories)
                if category is None:
                    continue
                for cells in rows:
                    if len(cells) < 2:
                        continue
                    title, price_raw = cells[0], cells[1]
                    title_clean = title.strip()
                    # Пустые/мусорные/заголовочные строки донора пропускаем.
                    if (
                        len(title_clean) < 3
                        or title_clean in ('+L', '+')
                        or title_clean.lower() == 'наименование'
                    ):
                        continue
                    for bad, good in TITLE_FIXES.items():
                        title = title.replace(bad, good)
                    title = title.strip()
                    price = normalize_price(price_raw)
                    product, was_created = Product.objects.update_or_create(
                        title=title,
                        defaults={'price': price, 'category': category},
                    )
                    if not product.slug:
                        product.save()  # генерирует ЧПУ
                    if was_created:
                        created_count += 1
                    else:
                        updated_count += 1
        self.stdout.write(self.style.SUCCESS(
            f'Товары: создано {created_count}, обновлено {updated_count}.'
        ))

    def ensure_categories(self) -> dict:
        """Создаёт категории и привязывает услуги ремонта для CTA."""
        categories = {}
        for key, rule in CATEGORY_RULES:
            repair = None
            if rule['repair_slug']:
                repair = Service.objects.filter(slug=rule['repair_slug']).first()
            # Ключ — title (уникальное поле); slug генерирует save(), если пуст.
            category, _ = ProductCategory.objects.update_or_create(
                title=rule['title'],
                defaults={
                    'order': rule['order'],
                    'repair_service': repair,
                    'cta_title': rule['cta_title'],
                    'cta_text': rule['cta_text'],
                },
            )
            if not category.slug:
                category.save()
            categories[key] = category
        return categories

    def match_category(self, heading: str, categories: dict):
        if not heading:
            return None
        lowered = heading.lower()
        for key, category in categories.items():
            if key.lower() in lowered:
                return category
        return None

    # ---- Услуги -------------------------------------------------------

    def parse_services(self) -> None:
        html = fetch_html(f'{BASE_URL}/uslugi/')
        collected: dict = {}  # slug услуги -> [(name, price), ...]
        for heading, rows in parse_tables(html):
            for cells in rows:
                if not cells or cells[0].startswith('-'):
                    continue  # служебные примечания
                if len(cells) < 2:
                    continue
                name = cells[0].strip()
                unit = cells[1].strip() if len(cells) > 2 else ''
                price_raw = cells[2] if len(cells) > 2 else (cells[1] if len(cells) > 1 else '')
                price = normalize_price(price_raw) or (
                    'договорная' if 'договор' in price_raw.lower() else ''
                )
                if not name or not price:
                    continue
                slug = self.match_row(name, heading)
                if slug is None:
                    continue
                full_name = f'{name}, {unit}' if unit else name
                collected.setdefault(slug, []).append((full_name, price))
        # Прайс с донора дополняет курируемый прайс из seed: существующие
        # позиции (по имени) обновляются, новые добавляются, удалённые на
        # доноре позиции в каталоге остаются (их убирает seed_services).
        price_rows = 0
        with transaction.atomic():
            for slug, rows in collected.items():
                service = Service.objects.filter(slug=slug).first()
                if service is None:
                    continue
                seen_names = set()
                for full_name, price in rows:
                    # Уникальность (service, name): при дубле добавляем вариант.
                    variant = 2
                    base_name = full_name
                    while full_name in seen_names:
                        full_name = f'{base_name} (вариант {variant})'
                        variant += 1
                    seen_names.add(full_name)
                    ServicePrice.objects.update_or_create(
                        service=service, name=full_name, defaults={'price': price},
                    )
                    price_rows += 1
        self.stdout.write(self.style.SUCCESS(f'Услуги: записей прайса {price_rows}.'))

    def match_row(self, name: str, heading: str):
        """Сопоставляет строку прайса конкретной услуге (узел = своя карточка).

        None в правилах означает «услуга определяется по заголовку таблицы»
        (монтажные/сборочные работы без конкретного узла).
        """
        lowered = name.lower()
        for key, slug in ROW_RULES:
            if key in lowered:
                if slug is None:
                    return self.match_service(heading)
                return slug
        # Нераспознанные строки: относим по заголовку таблицы.
        return self.match_service(heading)

    def match_service(self, heading: str):
        if not heading:
            return None
        for key, slug in SERVICE_RULES:
            if key.lower() in heading.lower():
                return Service.objects.filter(slug=slug).first()
        return None
