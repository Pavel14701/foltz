from django.contrib import admin
from blog.models import BlogCategory, BlogTag, BlogPost, BlogPostSection
from common.models import Gallery, Image
from django.contrib.contenttypes.admin import GenericStackedInline

class BlogSectionInline(admin.TabularInline):
    model = BlogPostSection
    extra = 1

class GalleryInline(GenericStackedInline):
    model = Gallery
    extra = 1

class ImageInline(GenericStackedInline):
    model = Image
    extra = 1

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'category']
    list_filter = ['category']
    inlines = [BlogSectionInline]

class BlogSectionAdmin(admin.ModelAdmin):
    inlines = [GalleryInline, ImageInline]

admin.site.register(BlogCategory)
admin.site.register(BlogTag)
admin.site.register(BlogPost, BlogAdmin)
admin.site.register(BlogPostSection, BlogSectionAdmin)