from django.urls import path
from . import views

app_name = "services"

urlpatterns = [
    path('services/', views.services_view, name="services")
]