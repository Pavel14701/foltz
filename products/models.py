from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from slugify import slugify
from django.utils import timezone
from services.utils.json_validators import validate_characteristics, validate_service
import json
from common.models import Image, Gallery


class ProductCategory(models.Model):
    name = models.CharField('Имя категории', max_length=50)
    slug = models.SlugField('Url представление', blank=True, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def save(self, *args:tuple[any], **kwargs:dict[str, any]) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class ProductSubCategory(models.Model):
    name = models.CharField(
        verbose_name='Имя подкатегории',
        max_length=50
    )
    slug = models.SlugField(
        verbose_name='Url представление',
        blank=True,
        unique=True
    )
    category = models.ForeignKey(
        to=ProductCategory,
        on_delete=models.SET_NULL,
        verbose_name='К какой категории относится?',
        null = True
    )

    def save(self, *args:tuple[any], **kwargs:dict[str, any]) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class ProductTags(models.Model):
    name = models.CharField('Имя тега', max_length=50)
    slug = models.SlugField('Url представление', blank=True, unique=True)

    def save(self, *args:tuple[any], **kwargs:dict[str, any]) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name



class Product(models.Model):
    title = models.CharField('Заголовок товара', max_length=100, unique=True)
    preview_text = models.TextField(
        verbose_name='Краткое описание(превью)',
        max_length=200,
        blank=True,
        null=False
    )
    preview_video_url = models.URLField(
        verbose_name='Видео youtube(превью)',
        blank=True,
        null=True
    )
    preview_image =  GenericRelation(to=Image)
    category = models.ForeignKey(
        to=ProductCategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Какая категория?'
    )
    subcategory = models.ForeignKey(
        to=ProductSubCategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Какая подкатегория?'
    )
    price = models.IntegerField(
        verbose_name='Цена',
        null=True
    )
    slug = models.SlugField(
        verbose_name='Url представление',
        blank=True,
        unique=True)
    tags = models.ManyToManyField(
        verbose_name='Теги',
        to=ProductTags,
        blank=True)
    modified = models.DateTimeField(
        verbose_name='Дополнено',
        auto_now=True
    )
    quantity = models.IntegerField(
        verbose_name='Кол-во товара',
        null=True
    )

    def get_unique_slug(self) -> str:
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}{num}"
            num += 1
        return unique_slug

    def save(self, *args:tuple[any], **kwargs:dict[str, any]) -> None:
        if not self.slug:
            self.slug = self.get_unique_slug()
        super().save(*args, **kwargs)

    def delete(self, *args:tuple[any], **kwargs:dict[str, any]) -> None:
        if self.preview_image:
            images = Image.objects.filter(content_object=self)
            for image in images:
                related_objects = Image.objects.filter(content_type=image.content_type, object_id=image.object_id).exclude(pk=image.pk)
                # Проверка связи с BlogPostSection и удаление только в случае отсутствия других связей
                if related_objects.exists():
                    # Удалить только связь
                    image.content_object = None
                    image.save()
                elif image.content_type.model == 'product':
                    # Если связь только с BlogPostSection, удалить изображение и связь
                    image.delete()
        super().delete(*args, **kwargs)

    def get_related_products_from_json(self, json_data:str) -> list|list['Product']:
        data:dict = json.loads(json_data)
        title = data.get('title')
        category_name = data.get('category')
        subcategory_name = data.get('subcategory')
        if target_service := Product.objects.filter(
            title__icontains=title
        ).first():
            category = ProductCategory.objects.filter(name=category_name).first() if category_name else target_service.category
            subcategory = ProductSubCategory.objects.filter(name=subcategory_name).first() if subcategory_name else target_service.subcategory
            return (
                Product.objects.filter(category=category, subcategory=subcategory)
                .exclude(pk=target_service.pk)
                .distinct()
            )
        return []

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductSection(models.Model):
    order = models.PositiveIntegerField('Порядок', blank=True, null=True)
    subtitle = models.CharField('Подзаголовок', max_length=200, blank=True, null=True)
    content = models.TextField('Блок текста', blank=True, null=True)
    youtube_url = models.URLField('Видео youtube', blank=True, null=True)
    image = GenericRelation(to=Image)
    add = models.JSONField(
        verbose_name = 'JSON поле для рекламы(инфа для запроса)',
        validators=[validate_service],
        blank=True,
        null=True
    )
    characteristics = models.JSONField(
        verbose_name='Таблица характеристик',
        validators=[validate_characteristics],
        blank=True,
        null=True
    )
    product = models.ForeignKey(
        to=Product,
        related_name='product_section',
        on_delete=models.CASCADE,
        verbose_name='Какой товар?'
    )
    gallery = models.ForeignKey(
        to=Gallery,
        related_name='product_gallery',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

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
        if not self.order:
            max_order = ProductSection.objects.filter(product=self.product).aggregate(max_order=models.Max('order'))['max_order']
            self.order = max_order + 1 if max_order is not None else 1
        else:
            conflicting_sections = ProductSection.objects.filter(
                product=self.product, order=self.order
            ).exclude(
                pk=self.pk
            )
            if conflicting_sections.exists():
                conflicting_sections.update(
                    order=models.F('order') + 1
                )
        super().save(*args, **kwargs)
        self.product.modified = timezone.now()
        self.product.save()

    def delete(self, *args, **kwargs): 
        if self.image:
            images = Image.objects.filter(content_object=self)
            for image in images:
                related_objects = Image.objects.filter(content_type=image.content_type, object_id=image.object_id).exclude(pk=image.pk)
                # Проверка связи с BlogPostSection и удаление только в случае отсутствия других связей
                if related_objects.exists():
                    # Удалить только связь
                    image.content_object = None
                    image.save()
                elif image.content_type.model == 'productsection':
                    # Если связь только с BlogPostSection, удалить изображение и связь
                    image.delete()
        super().delete(*args, **kwargs)
        sections = ProductSection.objects.filter(product=self.product).order_by('order')
        for index, section in enumerate(sections, start=1):
            section.order = index 
            section.save()

    class Meta:
        ordering = ['order']
        verbose_name = 'Секция товара'
        verbose_name_plural = 'Секции товаров'