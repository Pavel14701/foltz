from django.contrib import admin
from products.models import ProductCategory, ProductSubCategory, ProductTags, Product, ProductSection, Gallery, Image
from django.contrib.contenttypes.admin import GenericStackedInline

class ProductSectionInline(admin.TabularInline):
    model = ProductSection
    extra = 1

class GalleryInline(GenericStackedInline):
    model = Gallery
    extra = 1

class ImageInline(GenericStackedInline):
    model = Image
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'subcategory']
    list_filter = ['category', 'subcategory']
    inlines = [ProductSectionInline]

class ProductSectionAdmin(admin.ModelAdmin):
    inlines = [GalleryInline, ImageInline]

admin.site.register(ProductCategory)
admin.site.register(ProductSubCategory)
admin.site.register(ProductTags)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductSection, ProductSectionAdmin)
