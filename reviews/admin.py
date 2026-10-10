from django.contrib import admin

from reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'date')
    list_filter = ('date',)
    search_fields = ('author', 'text')
