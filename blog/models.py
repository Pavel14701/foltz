from django.db import models
import os
from django.core.exceptions import ValidationError
from common.base_models import ObjectBaseModel, SectionsBase
from pytils.translit import slugify

def get_upload_to(instance, filename:str) -> str:
    if isinstance(instance, BlogPost):
        return os.path.join('static', 'posts', f'post_{instance.id}', filename)
    elif isinstance(instance, BlogPostSection):
        return os.path.join('static', 'posts', f'post_{instance.post.id}', 'sections', f'section_{instance.id}', filename)
    return os.path.join('static', 'uploads', filename)


# Тут разбивай как хочешь, я в душе не ебу по каким категориям тебе нужно бить
class BlogCategory(models.Model):
    name = models.CharField('Имя категории', max_length=50)
    slug = models.SlugField('Url предвтавление')
    modified = models.DateTimeField('Дополнено',auto_now=True)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


#Тэги это упоминания чего-то. Например: запчасти, способа ремонта, 
class BlogTag(models.Model):
    name = models.CharField('Имя тега блога', max_length=50)
    slug = models.SlugField('Url представление')

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['id']
        verbose_name = 'Тег блога'
        verbose_name_plural = 'Теги блога'

    def __str__(self):
        return self.name


class BlogPost(ObjectBaseModel):
    title = models.CharField(max_length=200, blank=True, null=False, unique=True)
    preview_image = models.ImageField(upload_to=get_upload_to, blank=True, null=True)
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

    def get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while BlogPost.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}{num}"
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        super().save(*args, **kwargs)


class BlogPostSection(SectionsBase):
    post = models.ForeignKey(
        to=BlogPost,
        related_name='blog_section',
        on_delete=models.CASCADE,
        verbose_name='К какому посту относится?'
    )
    image = models.ImageField(upload_to=get_upload_to, blank=True, null=True)
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
        verbose_name = 'Секция поста блога'
        verbose_name_plural = 'Секции постов блога'

    def __str__(self) -> str:
        return f"{self.post.title} - {self.order}"
