from django.contrib import admin
from services.models import Service, ServiceSection, Category, Tag

class SectionInline(admin.TabularInline):
    model = ServiceSection
    extra = 1

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview_image', 'price', 'category', 'modified')
    search_fields = ('title', 'category__name', 'tags__name')
    inlines = [SectionInline]
    filter_horizontal = ('tags',)


class SectionAdmin(admin.ModelAdmin):
    list_display = ('service', 'order', 'subtitle', 'content', 'image', 'youtube_url')
    search_fields = ('service__title', 'subtitle')
    list_filter = ('service',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'modified')
    search_fields = ('name',)
    list_filter = ('modified',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)

admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceSection, SectionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
