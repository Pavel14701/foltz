from django.db import models
import os
from django.core.exceptions import ValidationError
from common.base_models import ObjectBaseModel, SectionsBase
from pytils.translit import slugify

def get_upload_to(instance, filename):
    if isinstance(instance, Service):
        return os.path.join('static', 'services', f'service_{instance.title}', filename)
    elif isinstance(instance, ServiceSection):
        return os.path.join('static', 'services', f'service_{instance.service.id}', 'sections', f'section_{instance.id}', filename)
    return os.path.join('static', 'uploads', filename)


# В услугах разбивка на категории производится по марке техники
class Category(models.Model):
    name = models.CharField('Имя категории', max_length=50)
    slug = models.SlugField('Url предвтавление')
    modified = models.DateTimeField('Дополнено',auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


#Тэг это запчасть
class Tag(models.Model):
    name = models.CharField('Имя тега', max_length=50)
    slug = models.SlugField('Url представление')

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Service(ObjectBaseModel):
    title = models.CharField('Заголовок', max_length=200, unique=True)
    preview_image = models.ImageField('Преввью картинка', upload_to=get_upload_to, blank=True, null=True)
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Какая категория?'
    )
    price = models.IntegerField('Цена', null=True)
    slug = models.SlugField('Url представление')
    tags = models.ManyToManyField(Tag, blank=True)
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

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

class ServiceSection(SectionsBase):
    service = models.ForeignKey(
        to ='Service',
        related_name='service_section',
        on_delete=models.CASCADE,
        verbose_name='Какая услуга ?'
    )
    image = models.ImageField('Иллюстрация', upload_to=get_upload_to, blank=True, null=True)

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
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['order']
        verbose_name = 'Секция услуги'
        verbose_name_plural = 'Секции услуги'