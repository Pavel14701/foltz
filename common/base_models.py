from typing import Any, Optional, Iterable

from django.db import models
from django.core.exceptions import ValidationError


class ObjectBaseModel(models.Model):
    preview_text: str = models.TextField(max_length=500, blank=True, null=False)
    preview_video_url: str | None = models.URLField(blank=True, null=True)
    title: str
    preview_image: object

    def __str__(self) -> str:
        return self.title

    def clean(self):
        # Превью не обязательно, но нельзя использовать одновременно картинку и видео
        if self.preview_image and self.preview_video_url:
            raise ValidationError('Можно выбрать только одно: либо изображение, либо URL видео.')

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: Optional[str] = None,
        update_fields: Optional[Iterable[str]] = None,
        **kwargs: Any,
    ) -> None:
        self.clean()
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
            **kwargs
        )

    class Meta:
        abstract = True


class SectionsBase(models.Model):
    order: int = models.PositiveIntegerField()
    subtitle: str | None = models.CharField(max_length=200, blank=True, null=True)
    content: str | None = models.TextField(blank=True, null=True)
    youtube_url: str | None = models.URLField(blank=True, null=True)
    service: Any
    product: Any
    post: Any
    image: Any

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

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: Optional[str] = None,
        update_fields: Optional[Iterable[str]] = None,
        **kwargs: Any,
    ) -> None:
        self.clean()
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
            **kwargs
        )