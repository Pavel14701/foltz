from rest_framework import serializers
from products.models import Product, ProductSection


class ProductSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSection
        fields = '__all__'

    def validate(self, data:dict) -> None|dict: 
        section_type = data.get('section_type')
        valid_section_types = ['image_section', 'youtube_url_section', 'content_section', 'subtitle_section']
        if section_type not in valid_section_types:
            raise serializers.ValidationError("Invalid section type.")
        if section_type == 'image_section' and not data.get('image'):
            raise serializers.ValidationError("Image is required for image section.")
        if section_type == 'youtube_url_section' and not data.get('youtube_url'):
            raise serializers.ValidationError("YouTube URL is required for YouTube URL section.")
        if section_type == 'content_section' and not data.get('content'):
            raise serializers.ValidationError("Content is required for content section.")
        if section_type == 'subtitle_section' and not data.get('subtitle'):
            raise serializers.ValidationError("Subtitle is required for subtitle section.")
        # Проверка на наличие одновременно заполненных полей
        fields = [data.get('image'), data.get('youtube_url'), data.get('subtitle'), data.get('content')]
        filled_fields = [field for field in fields if field]
        if len(filled_fields) > 1:
            raise serializers.ValidationError("Only one field should be filled for the section.")
        return data


class ProductSerializer(serializers.ModelSerializer):
    sections = ProductSectionSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'