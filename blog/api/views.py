"""API статей блога: CRUD постов и управление их секциями."""
from typing import Any

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from blog.api.serializers import PostSerializer, SectionSerializer
from blog.models import Blog, BlogSection
from common.base_api_views import BaseSectionSearchView, BaseViewApiSet


class BlogViewSet(BaseViewApiSet):
    """CRUD статей: список, создание, обновление, удаление, получение секций."""

    queryset = Blog.objects.all()
    serializer_class = PostSerializer
    search_fields = ['title', 'id']

    def get_section_serializer(self, sections: Any, many: bool = False) -> BaseSerializer:
        return SectionSerializer(sections, many=many)

    def get_section_queryset(self, instance: Blog) -> Any:
        return BlogSection.objects.filter(post=instance)

    @action(detail=True, methods=['get'])
    def get_post_sections(self, request: Request, pk: int | None = None) -> Response:
        """Секции конкретной статьи."""
        return self.sections(request, pk)


class BlogSectionSearchView(BaseSectionSearchView):
    """Поиск, обновление, перемещение и создание секций статьи."""

    serializer_class = SectionSerializer

    def get_queryset(self):
        return BlogSection.objects.filter(
            post_id=self.kwargs['post_id'], id=self.kwargs['section_id'],
        )

    def get_parent_lookup(self) -> str:
        return 'post'

    def get_section_serializer(self, instance: BlogSection) -> BaseSerializer:
        """Сериализатор родительской статьи для объединённого ответа."""
        return PostSerializer(instance.post)

    def create_response_data(self, post_serializer, section_serializer) -> dict:
        return {'post': post_serializer.data, 'section': section_serializer.data}

    def get_target_section(self, instance: BlogSection, direction: str) -> BlogSection | Response:
        """Соседняя секция для перемещения (up/down)."""
        if direction == 'up':
            return BlogSection.objects.filter(
                post=instance.post, order__lt=instance.order,
            ).order_by('-order').first()
        if direction == 'down':
            return BlogSection.objects.filter(
                post=instance.post, order__gt=instance.order,
            ).order_by('order').first()
        return Response({'detail': 'Invalid direction'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def move_post_section(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Перемещение секции статьи вверх/вниз."""
        return self.move(request, *args, **kwargs)
    def create_response_data(
        self,
        post_serializer: PostSerializer,
        section_serializer: SectionSerializer
    ) -> dict[str, Any]:
        return {
            'post': post_serializer.data,
            'section': section_serializer.data
        }