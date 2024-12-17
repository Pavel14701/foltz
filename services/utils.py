import django_filters
from services.models import Service

class ServiceFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    tag = django_filters.CharFilter(field_name='tag__name', lookup_expr='icontains')

    class Meta:
        model = Service
        fields = ['title', 'category', 'tag']
