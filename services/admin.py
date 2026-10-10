from django.contrib import admin
from django.utils.html import format_html

from services.models import Service, ServicePrice, ServiceSection


class SectionPreviewMixin:
    """Миниатюра картинки секции в форме конструктора."""

    @admin.display(description='Превью картинки')
    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="max-height:120px;border-radius:8px" />', obj.image.url)
        return '—'


class ServiceSectionInline(SectionPreviewMixin, admin.StackedInline):
    """Конструктор секций услуги."""

    model = ServiceSection
    extra = 1
    fields = ('order', 'subtitle', 'content', 'image', 'image_preview', 'youtube_url')
    readonly_fields = ('image_preview',)
    classes = ('collapse',)


class ServicePriceInline(admin.TabularInline):
    """Прайс услуги прямо на странице услуги."""

    model = ServicePrice
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Услуги: конструктор секций и прайса, картинки с удалением/заменой."""

    list_display = ('title', 'slug', 'preview_image')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ServiceSectionInline, ServicePriceInline]

    fieldsets = (
        ('Контент', {
            'fields': ('title', 'slug', 'preview_text', 'preview_image', 'preview_video_url'),
        }),
    )


@admin.register(ServiceSection)
class ServiceSectionAdmin(admin.ModelAdmin):
    """Секции услуг (отдельный список — для точечных правок)."""

    list_display = ('service', 'order', 'subtitle', 'content', 'image', 'youtube_url')
    search_fields = ('service__title', 'subtitle')
    list_filter = ('service',)
