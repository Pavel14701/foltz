from abc import ABC, abstractmethod
from typing import Any, Optional

from rest_framework import viewsets, filters, status 
from rest_framework.response import Response 
from rest_framework.exceptions import NotFound 
from rest_framework.request import Request 

class BaseViewApiSet(viewsets.ModelViewSet, ABC):
    """
    Абстрактный базовый ViewSet для работы с моделями, содержащими связанные секции.
    Поддерживает стандартные CRUD-операции и метод получения секций.
    """
    queryset = None
    serializer_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = None

    def sections(self, request: Request, pk: Optional[int] = None) -> Response:
        """
        Получает связанные секции для текущего объекта.
        """
        instance = self.get_object()
        sections = self.get_section_queryset(instance)
        serializer = self.get_section_serializer(sections, many=True)
        return Response(serializer.data)

    @abstractmethod
    def get_section_queryset(self, instance) -> Any:
        """
        Абстрактный метод: QuerySet секций, привязанных к объекту.
        """
        raise NotImplementedError

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Создаёт новый объект модели на основе сериализованных данных.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @abstractmethod
    def get_section_serializer(self, sections, many: bool):
        """
        Абстрактный метод, возвращающий сериализатор для секций.
        Должен быть реализован в наследнике.
        """
        pass

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Обновляет существующий объект модели.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Частично обновляет объект модели.
        """
        return self.update(request, *args, partial=True, **kwargs)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Удаляет объект модели.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Возвращает список объектов модели, с поддержкой пагинации и фильтрации.
        """
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response({'detail': 'No available objects'}, status=status.HTTP_204_NO_CONTENT)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BaseSectionSearchView(viewsets.ModelViewSet, ABC):
    """
    Абстрактный ViewSet для работы с секциями модели: поиск, обновление, перемещение и создание.
    """

    serializer_class = None

    @abstractmethod
    def get_queryset(self):
        """
        Абстрактный метод, возвращающий QuerySet с секциями.
        """
        pass

    @abstractmethod
    def get_section_serializer(self, instance):
        """
        Абстрактный метод, возвращающий сериализатор секции для передачи клиенту.
        """
        pass

    @abstractmethod
    def create_response_data(self, model_serializer, section_serializer) -> dict:
        """
        Абстрактный метод, возвращающий структуру данных для ответа retrieve-запроса.
        """
        pass

    @abstractmethod
    def get_target_section(self, instance, direction: Any):
        """
        Абстрактный метод, определяющий соседнюю секцию для перемещения.
        """
        pass

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Получает секцию и возвращает объединённый ответ сериализаторов.
        """
        instance = self.get_queryset().first()
        if not instance:
            raise NotFound("Section not found.")
        model_serializer = self.get_section_serializer(instance)
        section_serializer = self.get_serializer(instance)
        response_data = self.create_response_data(model_serializer, section_serializer)
        return Response(response_data)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Обновляет секцию. Частичное обновление поддерживается через `partial_update`.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_queryset().first()
        if not instance:
            raise NotFound("Section not found.")
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Частично обновляет секцию (PATCH).
        """
        return self.update(request, *args, partial=True, **kwargs)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Удаляет секцию, если она найдена.
        """
        instance = self.get_queryset().first()
        if not instance:
            raise NotFound("Section not found.")
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def move(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Перемещает секцию вверх или вниз в зависимости от переданного направления.
        Меняет местами значения поля `order` двух секций.
        """
        direction = request.data.get('direction')
        instance = self.get_queryset().first()
        if not instance:
            raise NotFound("Section not found.")
        target_section = self.get_target_section(instance, direction)
        if isinstance(target_section, Response):
            return target_section
        if target_section is None:
            return Response({'detail': 'No adjacent section found'}, status=status.HTTP_404_NOT_FOUND)
        instance.order, target_section.order = target_section.order, instance.order
        instance.save()
        target_section.save()
        return Response(status=status.HTTP_200_OK)

    @abstractmethod
    def get_parent_lookup(self) -> str:
        """
        Абстрактный метод: имя FK-поля секции на родителя ('post', 'service', 'product').
        """
        raise NotImplementedError

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Создаёт секцию заданного типа (`section_type`) и привязывает её к родителю.
        """
        section_type = request.data.get('section_type')
        if not section_type:
            return Response({'error': 'Section type is required'}, status=status.HTTP_400_BAD_REQUEST)
        if section_type != 'image_section':
            return Response({'error': 'Invalid section type'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(**{self.get_parent_lookup(): self.kwargs['post_id']})
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
