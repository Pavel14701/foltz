from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from slugify import slugify
from common.models import Image, Gallery
from services.utils.json_validators import validate_characteristics, validate_service
from django.utils import timezone


# Тут разбивай как хочешь, я в душе не ебу по каким категориям тебе нужно бить
class BlogCategory(models.Model):
    name = models.CharField(verbose_name='Имя категории', max_length=50)
    slug = models.SlugField(verbose_name='Url предвтавление')
    modified = models.DateTimeField(verbose_name='Дополнено',auto_now=True)

    def save(self, *args:tuple[any], **kwargs:dict[str, any]) -> None:
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['pk']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


#Тэги это упоминания чего-то. Например: запчасти, способа ремонта, 
class BlogTag(models.Model):
    name = models.CharField('Имя тега блога', max_length=50)
    slug = models.SlugField('Url представление')
    modified = models.DateTimeField(verbose_name='Дополнено', auto_now=True)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['pk']
        verbose_name = 'Тег блога'
        verbose_name_plural = 'Теги блога'

    def __str__(self) -> str:
        return self.name


class BlogPost(models.Model):
    preview_text = models.TextField(
        verbose_name='Краткое описание(превью)',
        max_length=500,
        blank=True,
        null=False
    )
    preview_video_url = models.URLField(
        verbose_name='Видео youtube(превью)',
        blank=True,
        null=True
    )
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=200,
        blank=True,
        null=False,
        unique=True
    )
    preview_image =  GenericRelation(to=Image)
    category = models.ForeignKey(
        to=BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Какая категория?'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField('Url представление')
    tags = models.ManyToManyField(BlogTag, blank=True)
    modified = models.DateTimeField('Дополнено', auto_now=True)

    def clean(self) -> None:
        if self.preview_image and self.preview_video_url:
            raise ValidationError(
                'Можно выбрать только одно: \
                либо изображение, либо URL видео.'
            )
        if not self.preview_image and not self.preview_video_url:
            raise ValidationError(
                'Необходимо указать либо \
                изображение, либо URL видео.'
            )

    def get_unique_slug(self) -> str:
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while BlogPost.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}{num}"
            num += 1
        return unique_slug

    def save(self, *args:tuple[any], **kwargs:dict[str, any]) -> None:
        self.clean()
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
                elif image.content_type.model == 'blogpost':
                    # Если связь только с BlogPostSection, удалить изображение и связь
                    image.delete()
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['pk']
        verbose_name = 'Пост блога'
        verbose_name_plural = 'Посты блога'


class BlogPostSection(models.Model):
    post = models.ForeignKey(
        to=BlogPost,
        on_delete=models.CASCADE,
        verbose_name='К какому посту относится?'
    )
    order = models.PositiveIntegerField('Порядок')
    subtitle = models.CharField(verbose_name='Подзаголовок', max_length=200, blank=True, null=True)
    content = models.TextField(verbose_name='Блок текста', blank=True, null=True)
    youtube_url = models.URLField(verbose_name='Видео youtube', blank=True, null=True)
    image = GenericRelation(to=Image)
    gallery = models.ForeignKey(
        to=Gallery,
        related_name='blogpost_gallery',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    add = models.JSONField(
        verbose_name='JSON поле для рекламы(инфа для запроса)',
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

    def clean(self) -> None:
        fields = [self.image, self.youtube_url, self.subtitle, self.content, self.gallery]
        filled_fields = [field for field in fields if field]
        if len(filled_fields) > 1:
            raise ValidationError('Можно выбрать только одно поле для заполнения.')
        if not filled_fields:
            raise ValidationError('Необходимо заполнить хотя бы одно поле.')

    def save(self, *args, **kwargs):
        self.clean()
        if not self.order:
            max_order = BlogPostSection.objects.filter(post=self.post).aggregate(max_order=models.Max('order'))['max_order']
            self.order = max_order + 1 if max_order is not None else 1
        else:
            conflicting_sections = BlogPostSection.objects.filter(
                post=self.post, order=self.order
            ).exclude(
                pk=self.pk
            )
            if conflicting_sections.exists():
                conflicting_sections.update(
                    order=models.F('order') + 1
                )
        super().save(*args, **kwargs)
        self.post.modified = timezone.now()
        self.post.save()

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
                elif image.content_type.model == 'blogpostsection':
                    # Если связь только с BlogPostSection, удалить изображение и связь
                    image.delete()
        super().delete(*args, **kwargs)
        sections = BlogPostSection.objects.filter(post=self.post).order_by('order')
        for index, section in enumerate(sections, start=1):
            section.order = index
            section.save()

    def __str__(self) -> str:
        return f"{self.post.title} - {self.order}"

    class Meta:
        ordering = ['order']
        verbose_name = 'Секция поста блога'
        verbose_name_plural = 'Секции постов блога'
