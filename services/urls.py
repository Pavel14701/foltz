from django.urls import path
from services.views import ServiceFormView, ServicesViews
from services.utils.autocompletes import ServiceAutocomplete, CategoryAutocomplete,\
    SubCategoryAutocomplete, TagsAutocomplete


app_name = "services"

urlpatterns = [
    # Автокомплиты
    path('service-autocomplete/', ServiceAutocomplete.as_view(), name='service-autocomplete'),
    path('category-autocomplete/', CategoryAutocomplete.as_view(), name='category-autocomplete'),
    path('subcategory-autocomplete/', SubCategoryAutocomplete.as_view(), name='subcategory-autocomplete'),
    path('tag-autocomplete/', TagsAutocomplete.as_view(), name='tag-autocomplete'),
    # Отображение услуг
    path('services/', ServicesViews.as_view(), {'action': 'home_view'}, name="services"),
    path('services/<int:pk>/', ServicesViews.as_view(), {'action': 'get_service'}, name='service-detail'),
    path('autocomplete/', ServicesViews.as_view(), {'action': 'autocomplete'}, name='services-autocomplete'),
    path('services/<int:pk>/details/', ServicesViews.as_view(), {'action': 'get_service_details'}, name='service-details'),
]
