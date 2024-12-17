from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from services.models import Service, ServiceSection
from services.api.serializers import ServiceSerializer, ServiceSectionSerializer
from common.base_api_views import BaseViewApiSet, BaseSectionSearchView
from rest_framework import  filters
from django_filters.rest_framework import DjangoFilterBackend
from services.utils import ServiceFilter


class ServiceViewSet(BaseViewApiSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ServiceFilter
    search_fields = ['title', 'id', 'category__name', 'tag__name']

    def get_section_serializer(self, sections, many):
        return ServiceSectionSerializer(sections, many)

    @action(detail=True, methods=['get'])
    def get_service_section(self, request, pk):
        return self.sections(request, pk)


class ServiceSectionSearchView(BaseSectionSearchView):
    serializer_class = ServiceSectionSerializer

    def retrieve(self, request, service_id=None, section_id=None): 
        try: 
            service = Service.objects.get(id=service_id) 
        except Service.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)  
        try: 
            section = ServiceSection.objects.get(id=section_id, service=service)
        except ServiceSection.DoesNotExist: 
            return Response({'error': 'Section of post does not found'}, status=404)
        serializer = ServiceSectionSerializer(section) 
        return Response(serializer.data)

    def get_queryset(self):
        service_id = self.kwargs['post_id']
        section_id = self.kwargs['section_id']
        service = Service.objects.filter(id=service_id).first()
        if not service:
            raise NotFound("Post not found.")
        if not (section := ServiceSection.objects.filter(service=service, id=section_id).first()):
            raise NotFound("Section not found.")
        return ServiceSection.objects.filter(service=service, id=section_id)

    def get_section_serializer(self, instance):
        return ServiceSerializer(instance.post)

    def create_responce_data(self, post_serializer, section_serializer) -> dict:
        return {
            'post': post_serializer.data,
            'section': section_serializer.data
        }

    def get_target_section(self, instance: ServiceSection, direction: str) -> ServiceSection|Response:
        if direction == 'up':
            return ServiceSection.objects.filter(post=instance.service, order__lt=instance.order).order_by('-order').first()
        elif direction == 'down':
            return ServiceSection.objects.filter(post=instance.service, order__gt=instance.order).order_by('order').first()
        else:
            return Response({"detail": "Invalid direction"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def move_service_section(self, request, *args, **kwargs):
        return self.move(request, *args, **kwargs)