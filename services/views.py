from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from services.models import Service


def services_view(request: HttpRequest) -> HttpResponse:
    """Каталог услуг."""
    services = Service.objects.prefetch_related('service_section')
    return render(request, 'services/service_list.html', {'services': services})


def service_detail_view(request: HttpRequest, slug: str) -> HttpResponse:
    """Страница конкретной услуги."""
    service = get_object_or_404(
        Service.objects.prefetch_related('service_section'),
        slug=slug,
    )
    return render(request, 'services/service_detail.html', {'service': service})