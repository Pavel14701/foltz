from django.contrib import admin
from django.urls import path, include
from params import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from params.sitemap import StaticViewSitemap
from params.views import obtain_token, verify_token, refresh_token

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('privacy_policy/', views.privacy_policy, name='privacy'),
    path('terms_of_service/', views.terms_of_service, name='terms_of_service'),

    path('api/', include('site_api.urls', namespace='api')),

    path('', include('site_forms.urls', namespace='site_forms')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('services/', include('services.urls', namespace='services')),
    path('products/', include('products.urls', namespace='products')),


    path('get-image-url/<str:image_name>/', views.get_image_url, name='get_image_url'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', views.robots_txt, name='robots_txt'),

    path('api/token/', obtain_token, name='token_obtain'),
    path('api/token/verify/', verify_token, name='token_verify'),
    path('api/token/refresh/', refresh_token, name='token_refresh'),

]



# Static and media files configuration
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
