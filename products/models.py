from django.db import models
import os
from django.core.exceptions import ValidationError
from pytils.translit import slugify as translit_slugify
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


class ProductCategory(models.Model):
    """Категория каталога товаров (Амкодор, МТЗ, гидравлика, метизы…).

    Для каждой категории можно привязать услугу ремонта — на страницах
    товаров категории показывается CTA-блок с призывом на этот ремонт.
    """

    title = models.CharField('категория', max_length=200, unique=True)
    slug = models.SlugField('ЧПУ', max_length=220, unique=True, blank=True, null=True)
    order = models.PositiveIntegerField('порядок', default=0)
    repair_service = models.ForeignKey(
        'services.Service',
        verbose_name='услуга ремонта для CTA',
        related_name='product_categories',
        null=True, blank=True,
        on_delete=models.SET_NULL,
    )
    cta_title = models.CharField(
        'заголовок CTA', max_length=200, blank=True,
        help_text='Пусто — берётся стандартный текст для товаров.',
    )
    cta_text = models.TextField(
        'текст CTA', max_length=500, blank=True,
        help_text='Пусто — берётся стандартный текст для товаров.',
    )

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'категория товаров'
        verbose_name_plural = 'категории товаров'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = translit_slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    @property
    def repair_link(self) -> str:
        """Ссылка на страницу привязанной услуги ремонта (для CTA на товаре)."""
        if self.repair_service_id:
            from django.urls import reverse
            return reverse('services:service_detail', args=[self.repair_service.slug])
        return ''

    @property
    def cta_link_text(self) -> str:
        """Подпись ссылки CTA: «Подробнее об услуге …»."""
        return f'Подробнее: {self.repair_service.title}' if self.repair_service_id else ''


class Product(ObjectBaseModel):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField('ЧПУ', max_length=220, unique=True, blank=True, null=True)
    price = models.CharField(
        'цена', max_length=100, blank=True,
        help_text='Как на ценнике: «9 750 р.», «1900/2300 р.», «договорная».',
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True, blank=True,
        on_delete=models.SET_NULL,
    )
    preview_image = models.ImageField(upload_to=get_upload_to, blank=True, null=True)

    class Meta:
        verbose_name = 'товар (обменный фонд)'
        verbose_name_plural = 'товары (обменный фонд)'
        ordering = ['id']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = translit_slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def min_price(self) -> int:
        """Число для плашки «от N р.»: первая цена из строки, 0 если цены нет."""
        import re
        digits = re.sub(r'\D', ' ', self.price).split()
        return int(digits[0]) if digits else 0

class ProductSection(SectionsBase):
    product = models.ForeignKey('Product', related_name='product_section', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_to, blank=True, null=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'секция товара'
        verbose_name_plural = 'секции товаров'

    def __str__(self):
        return f"{self.product.title} - {self.order}"


    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)