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
    is_published = models.BooleanField('опубликована', default=True)
    show_cta = models.BooleanField('показывать CTA-блок', default=False)
    cta_title = models.CharField('заголовок CTA', max_length=200, blank=True, null=False)
    cta_text = models.TextField('текст CTA', max_length=500, blank=True, null=False)
    cta_position = models.PositiveIntegerField('показывать после секции №', blank=True, null=True, help_text='Номер секции, после которой вставить CTA-блок; пусто — в конце статьи.')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'

    def __str__(self) -> str:
        return self.title

    @property
    def meta_description(self) -> str:
        """Текст первого контентного раздела — для meta description статьи."""
        for section in self.blog_section.all():
            if section.content:
                return section.content
        return ''

    @property
    def end_gallery(self):
        """Галерея без привязки к секции — показывается в конце статьи."""
        return self.gallery_images.filter(section__isnull=True)

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

    @property
    def embed_url(self) -> str:
        """YouTube-ссылка, пригодная для вставки в iframe."""
        if self.youtube_url and 'watch?v=' in self.youtube_url:
            return self.youtube_url.replace('watch?v=', 'embed/')
        return self.youtube_url or ''



def upload_to_gallery(instance: 'BlogSectionImage', filename: str) -> str:
    if instance.post_id:
        base = os.path.join('static', 'posts', f'post_{instance.post_id}', 'gallery')
        if instance.section_id:
            base = os.path.join(base, f'section_{instance.section_id}')
        return os.path.join(base, filename)
    return os.path.join('static', 'uploads', filename)


class BlogSectionImage(ObjectBaseModel):
    """Картинка галереи статьи: привязана к секции или к статье в целом."""

    post = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='gallery_images',
        verbose_name='статья',
    )
    section = models.ForeignKey(
        BlogSection,
        on_delete=models.CASCADE,
        related_name='gallery',
        verbose_name='секция',
        blank=True,
        null=True,
        help_text='Не указана — галерея покажется в конце статьи.',
    )
    image = models.ImageField('картинка', upload_to=upload_to_gallery)
    order = models.PositiveIntegerField('порядок', default=0, help_text='Чем меньше число — тем раньше в галерее.')

    class Meta:
        ordering = ['order']
        verbose_name = 'картинка галереи'
        verbose_name_plural = 'галереи секций'

    def __str__(self) -> str:
        return f'{self.post} — картинка {self.order}'

    def clean(self):
        # У галереи нет preview-полей — базовая валидация ObjectBaseModel не применима.
        pass
