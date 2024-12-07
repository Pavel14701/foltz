from django.db import models
import os
from common.base_models import ObjectBaseModel, SectionsBase

def get_upload_to(instance, filename):
    if isinstance(instance, Post):
        return os.path.join('static', 'posts', f'post_{instance.id}', filename)
    elif isinstance(instance, Section):
        return os.path.join('static', 'posts', f'post_{instance.post.id}', 'sections', f'section_{instance.id}', filename)
    return os.path.join('static', 'uploads', filename)


class Post(ObjectBaseModel):
    title = models.CharField(max_length=200, blank=True, null=False)
    preview_image = models.ImageField(upload_to=get_upload_to, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Section(SectionsBase):
    post = models.ForeignKey('Post', related_name='post_section', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_to, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.post.title} - {self.order}"
