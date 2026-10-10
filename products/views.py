"""Страницы каталога товаров: список с поиском/фильтрами и карточка товара."""

from types import SimpleNamespace

from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from products.models import Product, ProductCategory

PRODUCTS_PER_PAGE = 12
PARTIAL_LIMIT = 60


def products_view(request: HttpRequest) -> HttpResponse:
    """Каталог товаров: поиск, фильтр по категориям, живой поиск (partial)."""
    products = (
        Product.objects
        .filter(slug__isnull=False)
        .select_related('category', 'category__repair_service')
        .order_by('category__order', 'id')
    )
    query = (request.GET.get('q') or '').strip()
    category_slug = (request.GET.get('category') or '').strip()
    if category_slug:
        # Фильтр категории — в SQL, пока products ещё queryset.
        products = products.filter(category__slug=category_slug)
    if query:
        # Поиск в Python: SQLite не делает icontains/LOWER регистронезависимыми
        # для кириллицы, а каталог небольшой — так надёжно на любой БД.
        query_lower = query.lower()
        products = [
            item for item in products
            if query_lower in item.title.lower()
            or query_lower in (item.preview_text or '').lower()
        ]

    if request.GET.get('partial'):
        # Живой поиск/фильтрация: одна порция без пагинации.
        return render(
            request,
            'products/_product_grid.html',
            {
                'products': products[:PARTIAL_LIMIT],
                'query': query,
                'category_slug': category_slug,
            },
        )

    paginator = Paginator(products, PRODUCTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page') or 1)
    categories = ProductCategory.objects.prefetch_related('products')
    return render(
        request,
        'products/product_list.html',
        {
            'page_obj': page_obj,
            'products': page_obj.object_list,
            'categories': categories,
            'query': query,
            'category_slug': category_slug,
        },
    )


def product_detail_view(request: HttpRequest, slug: str) -> HttpResponse:
    """Страница товара: галерея, описание, цена и CTA ремонта по категории."""
    product = get_object_or_404(
        Product.objects.select_related('category', 'category__repair_service'),
        slug=slug,
    )
    # Галерея: превью + картинки секций (шаблоны ждут объекты с атрибутом .image).
    gallery_items = []
    if product.preview_image:
        gallery_items.append(SimpleNamespace(image=product.preview_image))
    for section in product.product_section.all():
        if section.image:
            gallery_items.append(SimpleNamespace(image=section.image))
    return render(
        request,
        'products/product_detail.html',
        {
            'product': product,
            'gallery_items': gallery_items,
            'request_question': f'Заявка на запчасть: {product.title}',
        },
    )