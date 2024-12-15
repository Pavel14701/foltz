from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from products.models import Product, ProductSection
from products.api.serializers import ProductSerializer, ProductSectionSerializer
from common.base_api_views import BaseViewApiSet, BaseSectionSearchView


class ProductViewSet(BaseViewApiSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    search_fields = ['title', 'id']

    def get_section_serializer(self, sections, many):
        return ProductSectionSerializer(sections, many)

    @action(detail=True, methods=['get'])
    def get_service_section(self, request, pk):
        return self.sections(request, pk)


class ProductSectionSearchView(BaseSectionSearchView):
    serializer_class = ProductSectionSerializer

    def retrieve(self, request, service_id=None, section_id=None): 
        try: 
            service = Product.objects.get(id=service_id) 
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)  
        try: 
            section = ProductSection.objects.get(id=section_id, service=service)
        except ProductSection.DoesNotExist: 
            return Response({'error': 'Section of product does not found'}, status=404)
        serializer = ProductSectionSerializer(section) 
        return Response(serializer.data)

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        section_id = self.kwargs['section_id']
        product = Product.objects.filter(id=product_id).first()
        if not product:
            raise NotFound("Product not found.")
        if not (section := ProductSection.objects.filter(product=product, id=section_id).first()):
            raise NotFound("Section of product does not found.")
        return section

    def get_section_serializer(self, instance):
        return ProductSerializer(instance.post)

    def create_responce_data(self, product_serializer, section_serializer) -> dict:
        return {
            'product': product_serializer.data,
            'section': section_serializer.data
        }

    def get_target_section(self, instance: ProductSection, direction: str) -> ProductSection|Response:
        if direction == 'up':
            return ProductSection.objects.filter(product=instance.product, order__lt=instance.order).order_by('-order').first()
        elif direction == 'down':
            return ProductSection.objects.filter(post=instance.product, order__gt=instance.order).order_by('order').first()
        else:
            return Response({"detail": "Invalid direction"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def move_service_section(self, request, *args, **kwargs):
        return self.move(request, *args, **kwargs)

    def validate_section_type(self, request, section_type, serializer:ProductSectionSerializer):
        if section_type == 'image_section' and serializer.validated_data.get('image'):
            ProductSection.objects.create(product_id=request.data['product_id'], **serializer.validated_data)
        elif section_type == 'youtube_url_section' and serializer.validated_data.get('youtube_url'):
            ProductSection.objects.create(product_id=request.data['product_id'], **serializer.validated_data)
        elif section_type == 'content_section' and serializer.validated_data.get('content'):
            ProductSection.objects.create(product_id=request.data['product_id'], **serializer.validated_data)
        elif section_type == 'subtitle_section' and serializer.validated_data.get('subtitle'):
            ProductSection.objects.create(product_id=request.data['product_id'], **serializer.validated_data)
        else:
            raise serializers.ValidationError('Invalid section type or missing required fields.')

