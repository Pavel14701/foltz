from django.contrib import admin

from blog.models import Blog, BlogSection


class BlogSectionInline(admin.TabularInline):
    """Секции статьи прямо на странице статьи."""

    model = BlogSection
    extra = 1


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """Статьи блога."""

    list_display = ('title', 'slug', 'created_at')
    search_fields = ('title',)
    inlines = [BlogSectionInline]


@admin.register(BlogSection)
class BlogSectionAdmin(admin.ModelAdmin):
    """Секции статей."""

    list_display = ('post', 'order', 'subtitle', 'content', 'image', 'youtube_url')
    search_fields = ('post__title', 'subtitle')
    list_filter = ('post',)
