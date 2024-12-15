from rest_framework import viewsets, generics, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from products.models import Product, ProductSection
from products.api.serializers import ProductSerializer, SectionSerializer
from common.base_api_views import BaseViewApiSet, BaseSectionSearchView


class ProductViewSet(BaseViewApiSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    search_fields = ['title', 'id']

    def get_section_serializer(self, sections, many):
        return SectionSerializer(sections, many)



class SectionSearchView(BaseSectionSearchView):
    serializer_class = SectionSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        section_id = self.kwargs['section_id']
        post = Product.objects.filter(id=product_id).first()
        if not post:
            raise NotFound("Post not found.")
        if not (section := ProductSection.objects.filter(post=post, id=section_id).first()):
            raise NotFound("Section not found.")
        return section

    def get_section_serializer(self, instance):
        return ProductSerializer(instance.product)

    def create_responce_data(self, post_serializer, section_serializer) -> dict:
        return {
            'post': post_serializer.data,
            'section': section_serializer.data
        }

    def get_target_section(self, instance:ProductSection, direction:str) -> ProductSection|Response:
        if direction == 'up':
            return ProductSection.objects.filter(post=instance.product, order__lt=instance.order).order_by('-order').first()
        elif direction == 'down':
            return ProductSection.objects.filter(post=instance.product, order__gt=instance.order).order_by('order').first()
        else:
            return Response({"detail": "Invalid direction"}, status=status.HTTP_400_BAD_REQUEST)
