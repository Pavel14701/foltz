from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods


def home(request:HttpRequest) -> HttpResponse: 
    return render(request, 'home.html')

def about(request:HttpRequest) -> HttpResponse: 
    return render(request, 'about.html')

def privacy_policy(request:HttpRequest) -> HttpResponse: 
    return render(request, 'privacy_policy.html')

def terms_of_service(request:HttpRequest) -> HttpResponse:
    return render(request, 'terms_of_service.html')

@require_http_methods(["GET"])
def get_image_url(request:HttpRequest, image_name: str) -> JsonResponse:
    image_url = f'/static/images/{image_name}'
    return JsonResponse({'image_url': image_url})

@require_http_methods(["GET"])
def robots_txt(request:HttpRequest) -> HttpResponse:
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
