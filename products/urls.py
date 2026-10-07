from django.urls import path
from products import views
from products.api.views import ProductViewSet, ProductSectionSearchView

app_name = "products"

urlpatterns = [
    # Для получения списка продуктов
    path('api/products/',
        ProductViewSet.as_view({'get': 'list'}),
        name='product-list'),
    # Для создания нового продукта
    path('api/products/create/',
        ProductViewSet.as_view({'post': 'create'}), 
        name='product-create'),
    # Для получения информации о конкретном продукте
    path('api/products/<int:pk>/',
        ProductViewSet.as_view({'get': 'retrieve'}),
        name='product-detail'),
    # Для обновления продукта
    path('api/products/<int:pk>/update/',
        ProductViewSet.as_view({'put': 'update'}),
        name='product-update'),
    # Для частичного обновления продукта
    path('api/products/<int:pk>/partial_update/',
        ProductViewSet.as_view({'patch': 'partial_update'}),
        name='product-partial-update'),
    # Для удаления продукта
    path('api/products/<int:pk>/delete/',
        ProductViewSet.as_view({'delete': 'destroy'}),
        name='product-delete'),
    # Для получения всех секций продукта
    path('api/products/<int:pk>/sections/',
        ProductViewSet.as_view({'get': 'get_product_sections'}),
        name='product-sections'),
    # Для получения информации о секции продукта
    path('api/products/<int:post_id>/sections/<int:section_id>/', 
        ProductSectionSearchView.as_view({'get': 'retrieve'}), 
        name='product-section-detail'),
    # Для обновления секции продукта
    path('api/products/<int:post_id>/sections/<int:section_id>/update/', 
        ProductSectionSearchView.as_view({'put': 'update'}), 
        name='product-section-update'),
    # Для частичного обновления секции продукта
    path('api/products/<int:post_id>/sections/<int:section_id>/partial_update/', 
        ProductSectionSearchView.as_view({'patch': 'partial_update'}), 
        name='product-section-partial-update'),
    # Для удаления секции продукта
    path('api/products/<int:post_id>/sections/<int:section_id>/delete/', 
        ProductSectionSearchView.as_view({'delete': 'destroy'}), 
        name='product-section-delete'),
    # Для перемещения секции продукта
    path('api/products/<int:post_id>/sections/<int:section_id>/move/', 
        ProductSectionSearchView.as_view({'post': 'move_product_section'}), 
        name='product-section-move'),
    # Для создания новой секции продукта
    path('api/products/<int:post_id>/sections/create/', 
        ProductSectionSearchView.as_view({'post': 'create'}), 
        name='product-section-create'),
    # Отображение продуктов
    path('products/', views.products, name="products")
]