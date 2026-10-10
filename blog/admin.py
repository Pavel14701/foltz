from django import forms
from django.contrib import admin
from django.utils.html import format_html

from blog.models import Blog, BlogSection, BlogSectionImage


class BlogSectionInline(admin.StackedInline):
    """Конструктор секций статьи: заголовок, тексты, картинка, видео + порядок."""

    model = BlogSection
    extra = 1
    fields = ('order', 'subtitle', 'content', 'image', 'image_preview', 'youtube_url')
    readonly_fields = ('image_preview',)
    classes = ('collapse',)

    @admin.display(description='Превью картинки')
    def image_preview(self, obj: BlogSection | None):
        if obj and obj.image:
            return format_html('<img src="{}" style="max-height:120px;border-radius:8px" />', obj.image.url)
        return '—'


class BlogSectionImageInline(admin.TabularInline):
    """Галерея: несколько картинок для секций статьи."""

    model = BlogSectionImage
    extra = 3
    fields = ('section', 'image', 'image_preview', 'order')
    verbose_name = 'картинка галереи'
    verbose_name_plural = 'Галерея статьи (несколько картинок к секции или в конец статьи)'

    readonly_fields = ('image_preview',)

    class SectionChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            title = obj.subtitle or obj.content[:40] or f'Секция {obj.order}'
            return f'{obj.order}. {title}'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'section':
            kwargs['queryset'] = BlogSection.objects.select_related('post').order_by('post__title', 'order')
            kwargs['form_class'] = self.SectionChoiceField
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    @admin.display(description='Превью')
    def image_preview(self, obj: BlogSectionImage | None):
        if obj and obj.image:
            return format_html('<img src="{}" style="max-height:100px;border-radius:8px" />', obj.image.url)
        return '—'


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """Статьи блога: конструктор секций, публикация и CTA-блок."""

    list_display = ('title', 'slug', 'is_published', 'created_at')
    list_filter = ('is_published',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BlogSectionInline, BlogSectionImageInline]
    actions = ('make_published', 'make_unpublished')

    fieldsets = (
        ('Контент', {
            'fields': ('title', 'slug', 'preview_text', 'preview_image', 'preview_video_url'),
        }),
        ('Публикация и предпросмотр', {
            'fields': ('is_published',),
            'description': 'Снятая галочка — черновик: страница откроется только администратору для предпросмотра.',
        }),
        ('CTA-блок в статье', {
            'fields': ('show_cta', 'cta_title', 'cta_text', 'cta_position'),
            'classes': ('collapse',),
            'description': 'CTA встанет после указанной секции; если не указана — в конце статьи.',
        }),
    )

    @admin.action(description='Опубликовать выбранные статьи')
    def make_published(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description='Снять с публикации (черновик)')
    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)


@admin.register(BlogSection)
class BlogSectionAdmin(admin.ModelAdmin):
    """Секции статей (отдельный список — для точечных правок)."""

    list_display = ('post', 'order', 'subtitle', 'content', 'image', 'youtube_url')
    search_fields = ('post__title', 'subtitle')
    list_filter = ('post',)
    inlines = (BlogSectionImageInline,)
