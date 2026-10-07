from django.contrib import admin

from user.models import Message, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Профили пользователей."""

    list_display = ('user', 'username', 'email', 'created')
    search_fields = ('user__username', 'username', 'email')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Сообщения между пользователями."""

    list_display = ('sender', 'recipient', 'subject', 'is_read', 'created')
    search_fields = ('subject', 'body')
    list_filter = ('is_read',)
