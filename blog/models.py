import os
from typing import TYPE_CHECKING

from django.db import models
from pytils.translit import slugify as translit_slugify
from common.base_models import ObjectBaseModel, SectionsBase


if TYPE_CHECKING:
    from .models import Blog, BlogSection  # чтобы избежать циклических импортов

def upload_to_blog(instance: models.Model, filename: str) -> str:
    # Добавляем защиту от неожиданных типов
    if isinstance(instance, Blog):
        return os.path.join('static', 'posts', f'post_{instance.pk}', filename)
    return os.path.join('static', 'uploads', filename)

def upload_to_section(instance: models.Model, filename: str) -> str:
    # Безопасная проверка, что instance действительно BlogSection
    if isinstance(instance, BlogSection) and instance.pk and instance.post:
        return os.path.join(
            'static',
            'posts',
            f'post_{instance.post}',
            'sections',
            f'section_{instance.pk}',
            filename
        )
    return os.path.join('static', 'uploads', filename)


class Blog(ObjectBaseModel):
    title: str = models.CharField(max_length=200, blank=True, null=False, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True, null=True)
    preview_image = models.ImageField(upload_to=upload_to_blog, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title

    @property
    def meta_description(self) -> str:
        """Текст первого контентного раздела — для meta description статьи."""
        for section in self.blog_section.all():
            if section.content:
                return section.content
        return ''

    def save(self, *args, **kwargs):
        # ЧПУ для SEO: генерируем из заголовка, если slug не задан вручную
        if not self.slug:
            self.slug = translit_slugify(self.title)
        super().save(*args, **kwargs)


class BlogSection(SectionsBase):
    post = models.ForeignKey(Blog, related_name='blog_section', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to_section, blank=True, null=True)

    class Meta(SectionsBase.Meta):
        ordering = ['order']

    def __str__(self) -> str:
        return f"{self.post.title} - {self.order}"
