from django.urls import path
from .views import contact_view
from django.views.generic import TemplateView

app_name = 'site_forms'

urlpatterns = [
    path('contact/', contact_view, name='contact'),
    path('success/', TemplateView.as_view(template_name='site_forms/success.html'), name='success'),
]