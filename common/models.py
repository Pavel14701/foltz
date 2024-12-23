from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from slugify import slugify
import os

def get_upload_to(instance: models.Model, filename: str) -> str: 
    return os.path.join('media', 'site-images', f'{instance.pk}_{slugify(filename)}')

class Image(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    order = models.PositiveBigIntegerField(verbose_name='Порядок', null=True, blank=True)
    image = models.ImageField(upload_to=get_upload_to)
    description = models.CharField(verbose_name='Описание', max_length=200, blank=True, null=True)
    alt = models.CharField(verbose_name='Alt-тег', max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def get_unique_slug(self) -> str:
        identifier = f"{self.content_type.model}_{self.pk}"
        slug = slugify(identifier)
        unique_slug = slug
        num = 1
        while Image.objects.filter(slug=unique_slug).exists():
            num += 1
            unique_slug = f"{slug}-{num}"
        return unique_slug

    def save(self, *args, **kwargs):
        self.clean()
        if not self.slug:
            self.slug = self.get_unique_slug()
        super().save(*args, **kwargs)

    def clean(self) -> None:
        if not self.content_type or not self.object_id:
            raise ValidationError('Image must be related to a specific object with valid content type and ID.')

    def __str__(self) -> str:
        return f"Image {self.pk} linked to {self.content_object}"

    class Meta:
        verbose_name = 'Иллюстрация'
        verbose_name_plural = 'Иллюстрации'

class Gallery(models.Model):
    name = models.CharField(verbose_name='Описание галереи', max_length=200)
    created_at = models.DateTimeField(verbose_name='Создано:', auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    images = GenericRelation(Image, related_query_name='gallery')

    def delete(self, *args, **kwargs):
        images = Image.objects.filter(content_object=self)
        for image in images:
            gallery_images = Image.objects.filter(
                content_type=image.content_type,
                object_id=image.object_id
            )
            related_objects = gallery_images.exclude(pk=image.pk)
            if not related_objects.exists():
                image.delete()
        super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

