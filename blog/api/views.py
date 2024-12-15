from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from blog.models import Blog, BlogSection
from blog.api.serializers import PostSerializer, SectionSerializer
from common.base_api_views import BaseViewApiSet, BaseSectionSearchView


class BlogViewSet(BaseViewApiSet):
    queryset = Blog.objects.all()
    serializer_class = PostSerializer
    search_fields = ['title', 'id']

    def get_section_serializer(self, sections, many):
        return SectionSerializer(sections, many)

    @action(detail=True, methods=['get'])
    def get_post_section(self, request, pk):
        return self.sections(request, pk)


class BlogSectionSearchView(BaseSectionSearchView):
    serializer_class = SectionSerializer

    def retrieve(self, request, post_id=None, section_id=None):
        try: 
            post = Blog.objects.get(id=post_id) 
        except Blog.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)
        try: 
            section = BlogSection.objects.get(id=section_id, post=post)
        except BlogSection.DoesNotExist: 
            return Response({'error': 'Section of post does not found'}, status=404)
        serializer = SectionSerializer(section) 
        return Response(serializer.data)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        section_id = self.kwargs['section_id']
        post = Blog.objects.filter(id=post_id).first()
        if not post:
            raise NotFound("Post not found.")
        if not (section := BlogSection.objects.filter(post=post, id=section_id).first()):
            raise NotFound("Section not found.")
        return BlogSection.objects.filter(post=post, id=section_id)

    def get_section_serializer(self, instance):
        return PostSerializer(instance.post)

    def create_responce_data(self, post_serializer, section_serializer) -> dict:
        return {
            'post': post_serializer.data,
            'section': section_serializer.data
        }

    def get_target_section(self, instance: BlogSection, direction: str) -> BlogSection | Response:
        if direction == 'up':
            return BlogSection.objects.filter(post=instance.post, order__lt=instance.order).order_by('-order').first()
        elif direction == 'down':
            return BlogSection.objects.filter(post=instance.post, order__gt=instance.order).order_by('order').first()
        else:
            return Response({"detail": "Invalid direction"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def move_post_section(self, request, *args, **kwargs):
        return self.move(request, *args, **kwargs)

    def validate_section_type(self, request, section_type, serializer:SectionSerializer):
        if section_type == 'image_section' and serializer.validated_data.get('image'):
            BlogSection.objects.create(post_id=request.data['post_id'], **serializer.validated_data)
        elif section_type == 'youtube_url_section' and serializer.validated_data.get('youtube_url'):
            BlogSection.objects.create(post_id=request.data['post_id'], **serializer.validated_data)
        elif section_type == 'content_section' and serializer.validated_data.get('content'):
            BlogSection.objects.create(post_id=request.data['post_id'], **serializer.validated_data)
        elif section_type == 'subtitle_section' and serializer.validated_data.get('subtitle'):
            BlogSection.objects.create(post_id=request.data['post_id'], **serializer.validated_data)
        else:
            raise serializers.ValidationError('Invalid section type or missing required fields.')
