from rest_framework import serializers  # type: ignore
from blog.models import BlogSection, Blog
from typing import Any

class SectionSerializer(serializers.ModelSerializer):
    section_type = serializers.CharField(write_only=True)

    class Meta:
        model = BlogSection
        fields = ['order', 'subtitle', 'content', 'youtube_url', 'image', 'section_type']

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        section_type = attrs.get('section_type')
        valid_section_types = [
            'image_section', 
            'youtube_url_section', 
            'content_section', 
            'subtitle_section'
        ]
        if section_type not in valid_section_types:
            raise serializers.ValidationError("Invalid section type.")
        if section_type == 'image_section' and not attrs.get('image'):
            raise serializers.ValidationError("Image is required for image section.")
        if section_type == 'youtube_url_section' and not attrs.get('youtube_url'):
            raise serializers.ValidationError("YouTube URL is required for YouTube URL section.")
        if section_type == 'content_section' and not attrs.get('content'):
            raise serializers.ValidationError("Content is required for content section.")
        if section_type == 'subtitle_section' and not attrs.get('subtitle'):
            raise serializers.ValidationError("Subtitle is required for subtitle section.")
        # Проверка на наличие одновременно заполненных полей
        fields = [
            attrs.get('image'), 
            attrs.get('youtube_url'), 
            attrs.get('subtitle'), 
            attrs.get('content')
        ]
        filled_fields = [field for field in fields if field]
        if len(filled_fields) > 1:
            raise serializers.ValidationError("Only one field should be filled for the section.")
        return attrs


class PostSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(source='blog_section', many=True, read_only=True)

    class Meta:
        model = Blog
        fields = '__all__'
