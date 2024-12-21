from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from blog.models import BlogPost, BlogPostSection
from site_api.serializers import PostSerializer, SectionSerializer
from common.base_api_views import BaseViewApiSet, BaseSectionSearchView


class BlogViewSet(BaseViewApiSet):
    queryset = BlogPost.objects.all()
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
            post = BlogPost.objects.get(id=post_id) 
        except BlogPost.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)
        try: 
            section = BlogPostSection.objects.get(id=section_id, post=post)
        except BlogPostSection.DoesNotExist: 
            return Response({'error': 'Section of post does not found'}, status=404)
        serializer = SectionSerializer(section) 
        return Response(serializer.data)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        section_id = self.kwargs['section_id']
        post = BlogPost.objects.filter(id=post_id).first()
        if not post:
            raise NotFound("Post not found.")
        if not (section := BlogPostSection.objects.filter(post=post, id=section_id).first()):
            raise NotFound("Section not found.")
        return BlogPostSection.objects.filter(post=post, id=section_id)

    def get_section_serializer(self, instance):
        return PostSerializer(instance.post)

    def create_responce_data(self, post_serializer, section_serializer) -> dict:
        return {
            'post': post_serializer.data,
            'section': section_serializer.data
        }

    def get_target_section(self, instance: BlogPostSection, direction: str) -> BlogPostSection | Response:
        if direction == 'up':
            return BlogPostSection.objects.filter(post=instance.post, order__lt=instance.order).order_by('-order').first()
        elif direction == 'down':
            return BlogPostSection.objects.filter(post=instance.post, order__gt=instance.order).order_by('order').first()
        else:
            return Response({"detail": "Invalid direction"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def move_post_section(self, request, *args, **kwargs):
        return self.move(request, *args, **kwargs)