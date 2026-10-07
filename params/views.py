"""Общие страницы сайта: главная, статические, robots.txt."""
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


def home(request: HttpRequest) -> HttpResponse:
    """Главная страница."""
    return render(request, 'home.html')


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
