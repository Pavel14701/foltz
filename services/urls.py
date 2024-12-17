from django.urls import path
from services.views import ServiceFormView, ServicesViews
from services.api.views import ServiceViewSet, ServiceSectionSearchView
from services.autocompletes import ServiceAutocomplete, TagAutocomplete, CategoryAutocomplete


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


    path('services/search/', ServicesViews.as_view(), {'action': 'service_search'}, name='service-search'),
    path('service-autocomplete/', ServiceAutocomplete.as_view(), name='service-autocomplete'),
    path('category-autocomplete/', CategoryAutocomplete.as_view(), name='category-autocomplete'),
    path('tag-autocomplete/', TagAutocomplete.as_view(), name='tag-autocomplete'),



    # Отображение услуг
    path('services/', ServicesViews.as_view(), {'action': 'home_view'}, name="services"),
    path('services/<int:pk>/', ServicesViews.as_view(), {'action': 'get_service'}, name='service-detail'),
    path('autocomplete/', ServicesViews.as_view(), {'action': 'autocomplete'}, name='services-autocomplete'),
    path('services/<int:pk>/details/', ServicesViews.as_view(), {'action': 'get_service_details'}, name='service-details'),
]
