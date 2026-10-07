from django.contrib import admin

from products.models import Product, ProductSection


class ProductSectionInline(admin.TabularInline):
    """Секции продукта прямо на странице продукта."""

    model = ProductSection
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Продукты."""

    list_display = ('title', 'preview_image', 'preview_video_url')
    search_fields = ('title',)
    inlines = [ProductSectionInline]


@admin.register(ProductSection)
class ProductSectionAdmin(admin.ModelAdmin):
    """Секции продуктов."""

    list_display = ('product', 'order', 'subtitle', 'content', 'image', 'youtube_url')
    search_fields = ('product__title', 'subtitle')
    list_filter = ('product',)
