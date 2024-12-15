from django.urls import path, include
from services import views
from rest_framework.routers import DefaultRouter
from services.api.views import ServiceViewSet, SectionSearchView

app_name = "services"
router = DefaultRouter()
router.register(r'services', ServiceViewSet)


urlpatterns = [
    path('services/', views.form_view, name="services"),
    path('api/services', include(router.urls)),
    path('api/services/<int:pk>/sections/', ServiceViewSet.as_view({'get': 'sections'}), name='service-sections'),
    path('api/services/<int:service_id>/sections/<int:section_id>/', SectionSearchView.as_view(), name='service-section-detail'),
    path('api/services/<int:service_id>/sections/<int:section_id>/move/', SectionSearchView.as_view({'service': 'move'}), name='service-section-move'),
]