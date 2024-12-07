from django.contrib import admin
from .models import Post, Section

class SectionInline(admin.TabularInline):
    model = Section
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [SectionInline]


admin.site.register(Post, PostAdmin)
admin.site.register(Section)