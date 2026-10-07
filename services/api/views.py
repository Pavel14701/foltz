"""API услуг: CRUD услуг и управление их секциями."""
from typing import Any

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from common.base_api_views import BaseSectionSearchView, BaseViewApiSet
from services.api.serializers import ServiceSerializer, ServiceSectionSerializer
from services.models import Service, ServiceSection


class ServiceViewSet(BaseViewApiSet):
    """CRUD услуг: список, создание, обновление, удаление, получение секций."""

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    search_fields = ['title', 'id']

    def get_section_serializer(self, sections: Any, many: bool = False) -> BaseSerializer:
        return ServiceSectionSerializer(sections, many=many)

    def get_section_queryset(self, instance: Service) -> Any:
        return ServiceSection.objects.filter(service=instance)

    @action(detail=True, methods=['get'])
    def get_service_sections(self, request: Request, pk: int | None = None) -> Response:
        """Секции конкретной услуги."""
        return self.sections(request, pk)


class ServiceSectionSearchView(BaseSectionSearchView):
    """Поиск, обновление, перемещение и создание секций услуги."""

    serializer_class = ServiceSectionSerializer

    def get_queryset(self):
        return ServiceSection.objects.filter(
            service_id=self.kwargs['post_id'], id=self.kwargs['section_id'],
        )

    def get_parent_lookup(self) -> str:
        return 'service'

    def get_section_serializer(self, instance: ServiceSection) -> BaseSerializer:
        """Сериализатор родительской услуги для объединённого ответа."""
        return ServiceSerializer(instance.service)

    def create_response_data(self, service_serializer, section_serializer) -> dict:
        return {'service': service_serializer.data, 'section': section_serializer.data}

    def get_target_section(self, instance: ServiceSection, direction: str) -> ServiceSection | Response:
        """Соседняя секция для перемещения (up/down)."""
        if direction == 'up':
            return ServiceSection.objects.filter(
                service=instance.service, order__lt=instance.order,
            ).order_by('-order').first()
        if direction == 'down':
            return ServiceSection.objects.filter(
                service=instance.service, order__gt=instance.order,
            ).order_by('order').first()
        return Response({'detail': 'Invalid direction'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def move_service_section(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Перемещение секции услуги вверх/вниз."""
        return self.move(request, *args, **kwargs)
