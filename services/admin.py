from django.contrib import admin
from .models import Service, Section

class SectionInline(admin.TabularInline):
    model = Section
    extra = 1

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview_image', 'preview_video_url')
    search_fields = ('title',)
    inlines = [SectionInline]

class SectionAdmin(admin.ModelAdmin):
    list_display = ('service', 'order', 'subtitle', 'content', 'image', 'youtube_url')
    search_fields = ('service__title', 'subtitle')
    list_filter = ('service',)

admin.site.register(Service, ServiceAdmin)
admin.site.register(Section, SectionAdmin)