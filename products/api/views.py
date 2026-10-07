"""API продуктов: CRUD продуктов и управление их секциями."""
from typing import Any

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from common.base_api_views import BaseSectionSearchView, BaseViewApiSet
from products.api.serializers import ProductSerializer, ProductSectionSerializer
from products.models import Product, ProductSection


class ProductViewSet(BaseViewApiSet):
    """CRUD продуктов: список, создание, обновление, удаление, получение секций."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    search_fields = ['title', 'id']

    def get_section_serializer(self, sections: Any, many: bool = False) -> BaseSerializer:
        return ProductSectionSerializer(sections, many=many)

    def get_section_queryset(self, instance: Product) -> Any:
        return ProductSection.objects.filter(product=instance)

    @action(detail=True, methods=['get'])
    def get_product_sections(self, request: Request, pk: int | None = None) -> Response:
        """Секции конкретного продукта."""
        return self.sections(request, pk)


class ProductSectionSearchView(BaseSectionSearchView):
    """Поиск, обновление, перемещение и создание секций продукта."""

    serializer_class = ProductSectionSerializer

    def get_queryset(self):
        return ProductSection.objects.filter(
            product_id=self.kwargs['post_id'], id=self.kwargs['section_id'],
        )

    def get_parent_lookup(self) -> str:
        return 'product'

    def get_section_serializer(self, instance: ProductSection) -> BaseSerializer:
        """Сериализатор родительского продукта для объединённого ответа."""
        return ProductSerializer(instance.product)

    def create_response_data(self, product_serializer, section_serializer) -> dict:
        return {'product': product_serializer.data, 'section': section_serializer.data}

    def get_target_section(self, instance: ProductSection, direction: str) -> ProductSection | Response:
        """Соседняя секция для перемещения (up/down)."""
        if direction == 'up':
            return ProductSection.objects.filter(
                product=instance.product, order__lt=instance.order,
            ).order_by('-order').first()
        if direction == 'down':
            return ProductSection.objects.filter(
                product=instance.product, order__gt=instance.order,
            ).order_by('order').first()
        return Response({'detail': 'Invalid direction'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def move_product_section(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Перемещение секции продукта вверх/вниз."""
        return self.move(request, *args, **kwargs)
