import json
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from graphql_jwt.shortcuts import get_token, get_user_by_token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate


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
        "Disallow: /api/"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


@csrf_exempt
def obtain_token(request:HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        data:dict = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if user := authenticate(username=username, password=password):
            token = get_token(user)
            return JsonResponse({'token': token})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def verify_token(request:HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        data:dict = json.loads(request.body)
        token = data.get('token')
        try:
            user = get_user_by_token(token)
            return JsonResponse({'user': user.username})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def refresh_token(request:HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        data:dict = json.loads(request.body)
        token = data.get('token')
        try:
            user = get_user_by_token(token)
            new_token = get_token(user)
            return JsonResponse({'token': new_token})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)