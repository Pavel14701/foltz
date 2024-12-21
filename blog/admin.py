from django.contrib import admin
from .models import BlogPost,  BlogPostSection

class  BlogSectionInline(admin.TabularInline):
    model =  BlogPostSection
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [BlogSectionInline]


admin.site.register(BlogPost, PostAdmin)
admin.site.register(BlogPostSection)