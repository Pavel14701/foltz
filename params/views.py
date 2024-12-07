from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.http import HttpRequest, HttpResponse

def home(request:HttpRequest) -> HttpResponse: 
    return render(request, 'home.html')

def about(request:HttpRequest) -> HttpResponse: 
    return render(request, 'about.html')

def privacy_policy(request:HttpRequest) -> HttpResponse: 
    return render(request, 'privacy_policy.html')

def custom_error(request:HttpRequest, exception=None, status=500) -> HttpResponse: 
    status_str = str(status)
    context = { 
        'status_code': status,
        'digit_1': status_str[0],
        'digit_2': status_str[1],
        'digit_3': status_str[2], 
        'error_message': {
            400: 'BAD REQUEST',
            403: 'FORBIDDEN',
            404: 'NOT FOUND',
            500: 'SERVER ERROR' 
        }.get(status, 'UNKNOWN') 
    } 
    return render(request, 'error.html', context, status=status)

def trigger_error_400(request:HttpRequest) -> HttpResponse: 
    return custom_error(request, status=400) 

def trigger_error_403(request:HttpRequest) -> HttpResponse: 
    return custom_error(request, status=403)

def trigger_error_404(request:HttpRequest) -> HttpResponse:
    return custom_error(request, status=404)

def trigger_error_500(request:HttpRequest) -> HttpResponse:
    return custom_error(request, status=500)