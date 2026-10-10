import re

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from services.models import Service

SERVICES_PER_PAGE = 6


def services_view(request: HttpRequest) -> HttpResponse:
    """Каталог услуг: поиск, постраничная навигация, живой поиск (partial)."""
    all_services = Service.objects.prefetch_related('service_section', 'prices')
    services = all_services
    query = (request.GET.get('q') or '').strip()
    if query:
        # Фильтр в Python: SQLite не делает icontains регистронезависимым для кириллицы.
        query_lower = query.lower()
        services = [
            item for item in services
            if query_lower in item.title.lower()
            or query_lower in (item.preview_text or '').lower()
            or any(query_lower in price.name.lower() for price in item.prices.all())
        ]

    if request.GET.get('partial'):
        # Живой поиск: все совпадения одной порцией, без пагинации.
        page_obj = Paginator(services, 100).get_page(1)
        return render(
            request,
            'services/_service_grid.html',
            {'page_obj': page_obj, 'query': query},
        )

    paginator = Paginator(services, SERVICES_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page') or 1)
    services_with_prices = [s for s in all_services if s.prices.all()]
    return render(
        request,
        'services/service_list.html',
        {
            'page_obj': page_obj,
            'query': query,
            'services_with_prices': services_with_prices,
        },
    )


def service_detail_view(request: HttpRequest, slug: str) -> HttpResponse:
    """Страница конкретной услуги."""
    service = get_object_or_404(
        Service.objects.prefetch_related('service_section', 'prices'),
        slug=slug,
    )
    return render(
        request,
        'services/service_detail.html',
        {
            'service': service,
            'request_question': f'Заявка: {service.title}',
        },
    )