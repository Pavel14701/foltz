from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from services.models import Service, ServiceSection
from services.api.serializers import ServiceSerializer, SectionSerializer
from common.base_api_views import BaseViewApiSet, BaseSectionSearchView


class ServiceViewSet(BaseViewApiSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    search_fields = ['title', 'id']

    def get_section_serializer(self, sections, many):
        return SectionSerializer(sections, many)


class SectionSearchView(BaseSectionSearchView):
    serializer_class = SectionSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        section_id = self.kwargs['section_id']
        post = Service.objects.filter(id=post_id).first()
        if not post:
            raise NotFound("Post not found.")
        if not (section := ServiceSection.objects.filter(post=post, id=section_id).first()):
            raise NotFound("Section not found.")
        return section

    def get_section_serializer(self, instance):
        return ServiceSerializer(instance.post)

    def create_responce_data(self, model_serializer, section_serializer) -> dict:
        return {
            'service': model_serializer.data,
            'section': section_serializer.data
        }

    def get_target_section(self, instance:ServiceSection, direction:str) -> ServiceSection|Response:
        if direction == 'up':
            return ServiceSection.objects.filter(post=instance.service, order__lt=instance.order).order_by('-order').first()
        elif direction == 'down':
            return ServiceSection.objects.filter(post=instance.service, order__gt=instance.order).order_by('order').first()
        else:
            return Response({"detail": "Invalid direction"}, status=status.HTTP_400_BAD_REQUEST)
