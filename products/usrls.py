from django.urls import path
from products import views
from products.utils.autocompletes import ProductAutocomplete,\
    TagsAutocomplete, CategoryAutocomplete, SubCategoryAutocomplete

app_name = "products"

urlpatterns = [
    # Автокомплиты
    path('products-autocomplete/', ProductAutocomplete.as_view(), name='service-autocomplete'),
    path('category-autocomplete/', CategoryAutocomplete.as_view(), name='category-autocomplete'),
    path('subcategory-autocomplete/', SubCategoryAutocomplete.as_view(), name='subcategory-autocomplete'),
    path('tag-autocomplete/', TagsAutocomplete.as_view(), name='tag-autocomplete'),
    # Отображение продуктов
    path('', views.products, name="products")
]