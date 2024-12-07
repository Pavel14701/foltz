from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import handler404, handler500, handler403, handler400
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('privacy_policy/', views.privacy_policy, name='privacy'),
    path('400/', views.trigger_error_400),
    path('403/', views.trigger_error_403),
    path('404/', views.trigger_error_404),
    path('500/', views.trigger_error_500),
    path('blog/', include('blog.urls')),
    path('services/', include('services.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +\
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

errors = [handler400, handler403, handler404, handler500]
for error in errors:
    error = 'params.views.custom_error'