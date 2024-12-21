from django.urls import path
from blog import views

app_name = "blog"

urlpatterns = [
    # Отображение блога
    path('', views.blog, name="blog")
]