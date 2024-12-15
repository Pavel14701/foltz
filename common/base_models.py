from django.db import models
from django.core.exceptions import ValidationError


class ObjectBaseModel(models.Model):
    preview_text = models.TextField(max_length=500, blank=True, null=False)
    preview_video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    def clean(self):
        if self.preview_image and self.preview_video_url:
            raise ValidationError('Можно выбрать только одно: либо изображение, либо URL видео.')
        if not self.preview_image and not self.preview_video_url:
            raise ValidationError('Необходимо указать либо изображение, либо URL видео.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True

class SectionsBase(models.Model):
    order = models.PositiveIntegerField()
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ['order']

    def __str__(self):
        classname = self.__class__.__name__
        if classname == 'Service':
            return f"{self.service.title} - {self.order}"
        elif classname == 'Product':
            return f"{self.product.title} - {self.order}"
        return f"{self.post.title} - {self.order}"

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