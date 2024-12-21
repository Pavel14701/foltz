from django.db import models
from django.core.exceptions import ValidationError
from pytils.translit import slugify
from django.utils import timezone
from services.utils.json_validators import validate_characteristics, validate_service
import os, json



def get_upload_to(instance, filename): 
    if isinstance(instance, Service):
        return os.path.join('media', 'services', f'service_{instance.title}', filename)
    elif isinstance(instance, ServiceSection):
        return os.path.join('media', 'services', f'service_{instance.service.pk}', 'sections', f'section_{instance.pk}', filename) 
    return os.path.join('media', 'uploads', filename)


class ServiceCategory(models.Model):
    name = models.CharField('Имя категории', max_length=50)
    slug = models.SlugField('Url представление', blank=True, unique=True)


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class ServiceSubCategory(models.Model):
    name = models.CharField('Имя подкатегории', max_length=50)
    slug = models.SlugField('Url представление', blank=True, unique=True)
    category = models.ForeignKey(
        to=ServiceCategory,
        on_delete=models.SET_NULL,
        verbose_name='К какой категории относится?'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class ServiceTags(models.Model):
    name = models.CharField('Имя тега', max_length=50)
    slug = models.SlugField('Url представление', blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name



class Service(models.Model):
    title = models.CharField('Заголовок', max_length=100, unique=True)
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
    preview_image = models.ImageField(
        verbose_name='Преввью картинка',
        upload_to=get_upload_to,
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        to=ServiceCategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Какая категория?'
    )
    subcategory = models.ForeignKey(
        to=ServiceSubCategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Какая подкатегория?'
    )
    price = models.IntegerField('Цена', null=True)
    slug = models.SlugField('Url представление', blank=True, unique=True)
    tags = models.ManyToManyField(ServiceTags, blank=True)
    modified = models.DateTimeField('Дополнено', auto_now=True)

    def get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Service.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}{num}"
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        super().save(*args, **kwargs)

    def get_related_services_from_json(self, json_data):
        data:dict = json.loads(json_data)
        title = data.get('title')
        category_name = data.get('category')
        subcategory_name = data.get('subcategory')
        if target_service := Service.objects.filter(
            title__icontains=title
        ).first():
            category = ServiceCategory.objects.filter(name=category_name).first() if category_name else target_service.category
            subcategory = ServiceSubCategory.objects.filter(name=subcategory_name).first() if subcategory_name else target_service.subcategory
            return (
                Service.objects.filter(category=category, subcategory=subcategory)
                .exclude(pk=target_service.pk)
                .distinct()
            )
        return []

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'



class ServiceSection(models.Model):
    order = models.PositiveIntegerField('Порядок', blank=True, null=True)
    subtitle = models.CharField('Подзаголовок', max_length=200, blank=True, null=True)
    content = models.TextField('Блок текста', blank=True, null=True)
    youtube_url = models.URLField('Видео youtube', blank=True, null=True)
    image = models.ImageField('Иллюстрация', upload_to=get_upload_to, blank=True, null=True)
    add = models.JSONField(
        verbose_name = 'JSON поле для рекламы(инфа для запроса)',
        validators=[validate_service],
        blank=True,
        null=True
    )
    characteristics = models.JSONField(
        verbose_name='Таблица',
        validators=[validate_characteristics],
        blank=True,
        null=True
    )
    service = models.ForeignKey(
        to=Service,
        related_name='service_section',
        on_delete=models.CASCADE,
        verbose_name='Какая услуга?'
    )

    def __str__(self):
        return f"{self.service.title} - {self.order}"

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
            max_order = ServiceSection.objects.filter(service=self.service).aggregate(max_order=models.Max('order'))['max_order']
            self.order = max_order + 1 if max_order is not None else 1
        else:
            conflicting_sections = ServiceSection.objects.filter(service=self.service, order=self.order).exclude(pk=self.pk)
            if conflicting_sections.exists():
                conflicting_sections.update(order=models.F('order') + 1)
        super().save(*args, **kwargs)
        self.service.modified = timezone.now()
        self.service.save()

    def delete(self, *args, **kwargs): 
        super().delete(*args, **kwargs)
        # Обновление порядка у оставшихся секций 
        sections = ServiceSection.objects.filter(service=self.service).order_by('order')
        for index, section in enumerate(sections, start=1):
            section.order = index 
            section.save()

    class Meta:
        ordering = ['order']
        verbose_name = 'Секция услуги'
        verbose_name_plural = 'Секции услуги'