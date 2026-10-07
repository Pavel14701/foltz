from django.db import models
from django.core.exceptions import ValidationError
from pytils.translit import slugify as translit_slugify
import os
from common.base_models import ObjectBaseModel, SectionsBase

def get_upload_to(instance, filename):
    if isinstance(instance, Service):
        return os.path.join('static', 'services', f'service_{instance.title}', filename)
    elif isinstance(instance, ServiceSection):
        return os.path.join('static', 'services', f'service_{instance.service.id}', 'sections', f'section_{instance.id}', filename)
    return os.path.join('static', 'uploads', filename)


class Service(ObjectBaseModel):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True, null=True)
    preview_image = models.ImageField(upload_to=get_upload_to, blank=True, null=True)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        # ЧПУ для SEO: генерируем из заголовка, если slug не задан вручную
        if not self.slug:
            self.slug = translit_slugify(self.title)
        super().save(*args, **kwargs)


class ServiceSection(SectionsBase):
    service = models.ForeignKey('Service', related_name='service_section', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_to, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.service.title} - {self.order}"

    @property
    def embed_url(self) -> str:
        """YouTube-ссылка, пригодная для вставки в iframe."""
        if self.youtube_url and 'watch?v=' in self.youtube_url:
            return self.youtube_url.replace('watch?v=', 'embed/')
        return self.youtube_url or ''

    def clean(self):
        fields = [self.image, self.youtube_url, self.subtitle, self.content]
        filled_fields = [field for field in fields if field]
        if len(filled_fields) > 1:
            raise ValidationError('Можно выбрать только одно поле для заполнения.')
        if not filled_fields:
            raise ValidationError('Необходимо заполнить хотя бы одно поле.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)