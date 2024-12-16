from django.urls import path
from services import views
from services.api.views import ServiceViewSet, ServiceSectionSearchView

app_name = "services"

urlpatterns = [
    # Для получения списка услуг
    path('api/services/',
        ServiceViewSet.as_view({'get': 'list'}),
        name='service-list'),
    # Для создания новой услуги
    path('api/services/create/',
        ServiceViewSet.as_view({'post': 'create'}), 
        name='service-create'),
    # Для получения информации о конкретной услуге
    path('api/services/<int:pk>/',
        ServiceViewSet.as_view({'get': 'retrieve'}),
        name='service-detail'),
    # Для обновления услуги
    path('api/services/<int:pk>/update/',
        ServiceViewSet.as_view({'put': 'update'}),
        name='service-update'),
    # Для частичного обновления услуги
    path('api/services/<int:pk>/partial_update/',
        ServiceViewSet.as_view({'patch': 'partial_update'}),
        name='service-partial-update'),
    # Для удаления услуги
    path('api/services/<int:pk>/delete/',
        ServiceViewSet.as_view({'delete': 'destroy'}),
        name='service-delete'),
    # Для получения всех секций услуги
    path('api/services/<int:pk>/sections/',
        ServiceViewSet.as_view({'get': 'get_service_sections'}),
        name='service-sections'),
    # Для получения информации о секции услуги
    path('api/services/<int:post_id>/sections/<int:section_id>/', 
        ServiceSectionSearchView.as_view({'get': 'retrieve'}), 
        name='service-section-detail'),
    # Для обновления секции услуги
    path('api/services/<int:post_id>/sections/<int:section_id>/update/', 
        ServiceSectionSearchView.as_view({'put': 'update'}), 
        name='service-section-update'),
    # Для частичного обновления секции услги
    path('api/services/<int:post_id>/sections/<int:section_id>/partial_update/', 
        ServiceSectionSearchView.as_view({'patch': 'partial_update'}), 
        name='service-section-partial-update'),
    # Для удаления секции услуги
    path('api/services/<int:post_id>/sections/<int:section_id>/delete/', 
        ServiceSectionSearchView.as_view({'delete': 'destroy'}), 
        name='service-section-delete'),
    # Для перемещения секции услгуи
    path('api/services/<int:post_id>/sections/<int:section_id>/move/', 
        ServiceSectionSearchView.as_view({'post': 'move_service_section'}), 
        name='service-section-move'),
    # Для создания новой секции услуги
    path('api/services/<int:post_id>/sections/create/', 
        ServiceSectionSearchView.as_view({'post': 'create'}), 
        name='service-section-create'),
    # Отображение услуг
    path('services/', views.services_view, name="services")
]