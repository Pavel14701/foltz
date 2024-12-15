from django.urls import path, include
from blog import views
from rest_framework.routers import DefaultRouter
from products.api.views import ProductViewSet, SectionSearchView

app_name = "products"
router = DefaultRouter()
router.register(r'posts', ProductViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/products/<int:pk>/sections/', ProductViewSet.as_view(extra={'get': 'sections'}), name='product-sections'),
    path('api/products/<int:product_id>/sections/<int:section_id>/', SectionSearchView.as_view(), name='product-section-detail'),
    path('api/products/<int:product_id>/sections/<int:section_id>/move/', SectionSearchView.as_view(extra={'product': 'move'}), name='product-section-move'),
    path('products/', views.blog, name="blog")
]
