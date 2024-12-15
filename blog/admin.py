from django.contrib import admin
from .models import Blog,  BlogSection

class  BlogSectionInline(admin.TabularInline):
    model =  BlogSection
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [BlogSectionInline]


admin.site.register(Blog, PostAdmin)
admin.site.register(BlogSection)