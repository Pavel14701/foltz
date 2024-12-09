from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import handler404, handler500, handler403, handler400
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .sitemap import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('privacy_policy/', views.privacy_policy, name='privacy'),
    path('terms_of_service/', views.terms_of_service, name='terms_of_service'),
    path('get-image-url/<str:image_name>/', views.get_image_url, name='get_image_url'),
    path('400/', views.trigger_error_400),
    path('403/', views.trigger_error_403),
    path('404/', views.trigger_error_404),
    path('500/', views.trigger_error_500),
    path('blog/', include('blog.urls', namespace='blog')),
    path('services/', include('services.urls', namespace='services')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]


errors = [handler400, handler403, handler404, handler500]
for error in errors:
    error = 'params.views.custom_error'


# Static and media files configuration
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
