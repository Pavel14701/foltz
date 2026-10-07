"""Маршруты API продуктов (JWT-защищённые, для бота и админ-панели)."""
from django.urls import path

from products.api.views import ProductSectionSearchView, ProductViewSet

app_name = 'products'

urlpatterns = [
    # Список продуктов
    path('api/products/',
        ProductViewSet.as_view({'get': 'list'}),
        name='product-list'),
    # Создание нового продукта
    path('api/products/create/',
        ProductViewSet.as_view({'post': 'create'}),
        name='product-create'),
    # Информация о конкретном продукте
    path('api/products/<int:pk>/',
        ProductViewSet.as_view({'get': 'retrieve'}),
        name='product-detail'),
    # Обновление продукта
    path('api/products/<int:pk>/update/',
        ProductViewSet.as_view({'put': 'update'}),
        name='product-update'),
    # Частичное обновление продукта
    path('api/products/<int:pk>/partial_update/',
        ProductViewSet.as_view({'patch': 'partial_update'}),
        name='product-partial-update'),
    # Удаление продукта
    path('api/products/<int:pk>/delete/',
        ProductViewSet.as_view({'delete': 'destroy'}),
        name='product-delete'),
    # Секции конкретного продукта
    path('api/products/<int:pk>/sections/',
        ProductViewSet.as_view({'get': 'get_product_sections'}),
        name='product-sections'),
    # Информация о секции продукта
    path('api/products/<int:post_id>/sections/<int:section_id>/',
        ProductSectionSearchView.as_view({'get': 'retrieve'}),
        name='product-section-detail'),
    # Обновление секции продукта
    path('api/products/<int:post_id>/sections/<int:section_id>/update/',
        ProductSectionSearchView.as_view({'put': 'update'}),
        name='product-section-update'),
    # Частичное обновление секции продукта
    path('api/products/<int:post_id>/sections/<int:section_id>/partial_update/',
        ProductSectionSearchView.as_view({'patch': 'partial_update'}),
        name='product-section-partial-update'),
    # Удаление секции продукта
    path('api/products/<int:post_id>/sections/<int:section_id>/delete/',
        ProductSectionSearchView.as_view({'delete': 'destroy'}),
        name='product-section-delete'),
    # Перемещение секции продукта
    path('api/products/<int:post_id>/sections/<int:section_id>/move/',
        ProductSectionSearchView.as_view({'post': 'move_product_section'}),
        name='product-section-move'),
    # Создание секции продукта
    path('api/products/<int:post_id>/sections/create/',
        ProductSectionSearchView.as_view({'post': 'create'}),
        name='product-section-create'),
]
