"""Общие страницы сайта: главная, статические, robots.txt."""
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from products.models import Product
from services.models import Service
from blog.models import Blog

# Карточки услуг на главной: слаг услуги из БД + фоновое фото +(curated) описание.
SERVICE_CARDS = [
    {
        'slug': 'remont-importnoy-tehniki',
        'image': 'manitoo_pogr.jpg',
        'text': ('JCB, Manitou, Caterpillar, Case, New Holland, John Deere — диагностика, '
                 'ремонт узлов и ТО импортной сельхоз- и дорожно-строительной техники.'),
    },
    {
        'slug': 'remont-gidravliki-mtz',
        'image': 'amkodor_pogr_new.jpg',
        'text': ('Интегральные блоки ZMS Bosch Rexroth и гидрораспределители РП-70 '
                 'энергонасыщенных тракторов МТЗ 2822, 3022, 3522. Проверка на стенде.'),
    },
    {
        'slug': 'kapremont-dvigateley',
        'image': 'engine_jcb2.jpg',
        'text': ('Капитальный ремонт ДВС Deutz, JCB, Perkins, Detroit, Weichai: '
                 'расточка, шлифовка, сборка и испытания.'),
    },
    {
        'slug': 'remont-gidronasosov',
        'image': 'raspred_bosch.jpg',
        'text': ('Ремонт гидронасосов, гидромоторов, цилиндров и распределителей '
                 'импортной и отечественной техники. Проверка на стенде, обменный фонд.'),
    },
]

# Тексты карточек обменного фонда на главной (по порядку сида).
FUND_TEXTS = [
    'Восстановленный шестерённый насос для МТЗ. Проверен на стенде, готов к установке.',
    'Секционный распределитель для тракторов МТЗ. Притирка золотников, испытан под давлением.',
    'Гидромотор для дорожной техники Амкодор. Проверен на стенде, гарантия 6 месяцев.',
]

FUND_IMAGES = ['manitoo_pogr.jpg', 'amkodor_pogr_new.jpg', 'engine_jcb2.jpg']


def home(request: HttpRequest) -> HttpResponse:
    """Главная страница: hero, услуги с ценами, обменный фонд."""
    services = {s.slug: s for s in Service.objects.prefetch_related('prices')}
    service_cards = []
    for card in SERVICE_CARDS:
        service = services.get(card['slug'])
        service_cards.append({
            **card,
            'title': service.title if service else card['slug'],
            'slug': card['slug'],
            'prices': list(service.prices.all()[:3]) if service else [],
            'min_price': service.min_price if service else None,
        })

    fund_products = [
        {
            'title': p.title.replace(' (обменный фонд)', ''),
            'image': FUND_IMAGES[i % len(FUND_IMAGES)],
            'text': FUND_TEXTS[i % len(FUND_TEXTS)],
        }
        for i, p in enumerate(Product.objects.all()[:3])
    ]

    return render(request, 'home.html', {
        'service_cards': service_cards,
        'fund_products': fund_products,
        'blog_posts': Blog.objects.prefetch_related('blog_section').all()[:3],
    })


def about(request: HttpRequest) -> HttpResponse:
    """Страница «О компании»."""
    return render(request, 'about.html')


def privacy_policy(request: HttpRequest) -> HttpResponse:
    """Политика конфиденциальности."""
    return render(request, 'privacy_policy.html')


def terms_of_service(request: HttpRequest) -> HttpResponse:
    """Условия использования."""
    return render(request, 'terms_of_service.html')


@require_http_methods(['GET'])
def get_image_url(request: HttpRequest, image_name: str) -> JsonResponse:
    """URL картинки из /static/images/ по имени (нужно для галереи и фонов на главной)."""
    return JsonResponse({'image_url': f'/static/images/{image_name}'})


def robots_txt(request: HttpRequest) -> HttpResponse:
    """robots.txt со ссылкой на sitemap."""
    lines = [
        'User-agent: *',
        'Disallow: /admin/',
        'Disallow: /api/',
        f'Sitemap: {request.build_absolute_uri("/sitemap.xml")}',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')
