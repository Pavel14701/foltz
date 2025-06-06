from django.db import models
import os
from common.base_models import ObjectBaseModel, SectionsBase

def get_upload_to(instance, filename:str) -> str:
    if isinstance(instance, Blog):
        return os.path.join('static', 'posts', f'post_{instance.id}', filename)
    elif isinstance(instance, BlogSection):
        return os.path.join('static', 'posts', f'post_{instance.post.id}', 'sections', f'section_{instance.id}', filename)
    return os.path.join('static', 'uploads', filename)


class Blog(ObjectBaseModel):
    title = models.CharField(max_length=200, blank=True, null=False, unique=True)
    preview_image = models.ImageField(upload_to=get_upload_to, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class BlogSection(SectionsBase):
    post = models.ForeignKey('Blog', related_name='blog_section', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_to, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self) -> str:
        return f"{self.post.title} - {self.order}"
