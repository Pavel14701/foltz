from rest_framework import viewsets, generics, filters, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from abc import abstractmethod, ABC


class BaseViewApiSet(viewsets.ModelViewSet, ABC):
    queryset = None
    serializer_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = None

    def sections(self, request, pk=None):
        model = self.get_object()
        sections = model.sections.all()
        serializer = self.get_section_serializer(sections, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @abstractmethod
    def get_section_serializer(self, sections, many):
        pass

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, partial=True, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BaseSectionSearchView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = None

    @abstractmethod
    def get_queryset(self):
        pass

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_queryset().first()
        if not instance:
            raise NotFound("Section not found.")
        model_serializer = self.get_section_serializer(instance)
        section_serializer = self.get_serializer(instance)
        response_data = self.create_responce_data(model_serializer, section_serializer)
        return Response(response_data)

    @abstractmethod
    def get_section_serializer(instance):
        pass

    @abstractmethod
    def create_responce_data(model_serializer, section_serializer) -> dict:
        pass

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_queryset().first()
        if not instance:
            raise NotFound("Section not found.")
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, partial=True, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_queryset().first()
        if not instance:
            raise NotFound("Section not found.")
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def move(self, request, *args, **kwargs):
        direction = request.data.get('direction')
        instance = self.get_queryset().first()
        if not instance:
            raise NotFound("Section not found.")
        if target_section:= self.get_target_section(instance, direction):
            instance.order, target_section.order = target_section.order, instance.order
            instance.save()
            target_section.save()
            return Response(status=status.HTTP_200_OK)        
        return Response({"detail": "Cannot move section in the specified direction"}, status=status.HTTP_400_BAD_REQUEST)


    @abstractmethod
    def get_target_section(self, instance, direction):
        pass

    def create(self, request, *args, **kwargs):
        section_type = request.data.pop('section_type', None)
        if section_type is None:
            return Response({'error': 'Section type is required'}, status=status.HTTP_400_BAD_REQUEST)

        if section_type == 'image_section':
            return self.image_section
        # Добавьте дополнительную логику для других типов секций, если нужно
        return Response({'error': 'Invalid section type'}, status=status.HTTP_400_BAD_REQUEST)


    def image_section(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def create(self, request, *args, **kwargs):
        section_type = request.data.get('section_type')
        if not section_type:
            return Response({'error': 'Section type is required'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.validate_section_type(request, section_type, serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @abstractmethod
    def validate_section_type(self, request, section_type, serializer):
        pass