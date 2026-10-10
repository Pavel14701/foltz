from django.contrib import admin
from django.utils.html import format_html

from products.models import Product, ProductCategory, ProductSection


class ProductSectionInline(admin.StackedInline):
    """Конструктор секций товара."""

    model = ProductSection
    extra = 1
    fields = ('order', 'subtitle', 'content', 'image', 'image_preview', 'youtube_url')
    readonly_fields = ('image_preview',)
    classes = ('collapse',)

    @admin.display(description='Превью картинки')
    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="max-height:120px;border-radius:8px" />', obj.image.url)
        return '—'


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    """Категории товаров и привязка CTA-блока ремонта."""

    list_display = ('title', 'slug', 'order', 'repair_service')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Категория', {'fields': ('title', 'slug', 'order')}),
        ('CTA-блок ремонта', {
            'description': 'Показывается на страницах товаров категории. '
                           'Пустые заголовок и текст — берутся стандартные.',
            'fields': ('repair_service', 'cta_title', 'cta_text'),
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Товары обменного фонда: конструктор секций, картинки."""

    list_display = ('title', 'category', 'price', 'preview_image')
    list_filter = ('category',)
    search_fields = ('title',)
    inlines = [ProductSectionInline]

    fieldsets = (
        ('Контент', {
            'fields': ('title', 'slug', 'category', 'price', 'preview_text', 'preview_image', 'preview_video_url'),
        }),
    )


@admin.register(ProductSection)
class ProductSectionAdmin(admin.ModelAdmin):
    """Секции товаров (отдельный список — для точечных правок)."""

    list_display = ('product', 'order', 'subtitle', 'content', 'image', 'youtube_url')
    search_fields = ('product__title', 'subtitle')
    list_filter = ('product',)
