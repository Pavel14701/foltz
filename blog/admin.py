from django.contrib import admin
from .models import Post,  BlogSection

class  BlogSectionInline(admin.TabularInline):
    model =  BlogSection
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [ BlogSectionInline]


admin.site.register(Post, PostAdmin)
admin.site.register( BlogSection)