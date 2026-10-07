from django.urls import path
from django.views.generic import TemplateView

from .views import contact_view

app_name = 'forms'

urlpatterns = [
    path('contact/', contact_view, name='contact'),
    path('success/', TemplateView.as_view(template_name='forms/success.html'), name='success'),
]
