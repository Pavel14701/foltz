from django.contrib import admin

from services.models import Service, ServiceSection


class ServiceSectionInline(admin.TabularInline):
    """Секции услуги прямо на странице услуги."""

    model = ServiceSection
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Услуги."""

    list_display = ('title', 'preview_image', 'preview_video_url')
    search_fields = ('title',)
    inlines = [ServiceSectionInline]


@admin.register(ServiceSection)
class ServiceSectionAdmin(admin.ModelAdmin):
    """Секции услуг."""

    list_display = ('service', 'order', 'subtitle', 'content', 'image', 'youtube_url')
    search_fields = ('service__title', 'subtitle')
    list_filter = ('service',)
