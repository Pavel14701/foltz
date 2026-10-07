from django.db import models
import os
from django.core.exceptions import ValidationError
from common.base_models import ObjectBaseModel, SectionsBase

def get_upload_to(instance, filename):
    """Путь загрузки превью товара и картинок его секций."""
    if isinstance(instance, Product):
        return os.path.join('static', 'products', f'product_{instance.pk}', filename)
    if isinstance(instance, ProductSection):
        return os.path.join(
            'static', 'products', f'product_{instance.product.pk}',
            'sections', f'section_{instance.pk}', filename,
        )
    return os.path.join('static', 'uploads', filename)


class Product(ObjectBaseModel):
    title = models.CharField(max_length=200, unique=True)
    preview_image = models.ImageField(upload_to=get_upload_to, blank=True, null=True)

class ProductSection(SectionsBase):
    product = models.ForeignKey('Product', related_name='product_section', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_to, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.product.title} - {self.order}"

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