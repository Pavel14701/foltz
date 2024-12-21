from django.contrib import admin
from services.models import Service, ServiceSection, ServiceCategory, ServiceSubCategory, ServiceTags

class SectionInline(admin.TabularInline):
    model = ServiceSection
    extra = 1

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview_image', 'price', 'category', 'subcategory', 'modified')
    search_fields = ('title', 'category__name', 'subcategory__name', 'tags__name')
    inlines = [SectionInline]
    filter_horizontal = ('tags',)
    exclude = ('slug',)

class ServiceSectionAdmin(admin.ModelAdmin):
    list_display = ('service', 'order', 'subtitle', 'content', 'image', 'youtube_url')
    search_fields = ('service__title', 'subtitle')
    list_filter = ('service',)

class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'modified')
    search_fields = ('name',)
    list_filter = ('modified',)
    exclude = ('slug',)

class ServiceSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    exclude = ('slug',)

class ServiceTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    exclude = ('slug',)

admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceSection, ServiceSectionAdmin)
admin.site.register(ServiceCategory, ServiceCategoryAdmin)
admin.site.register(ServiceSubCategory, ServiceSubCategoryAdmin)
admin.site.register(ServiceTags, ServiceTagAdmin)
