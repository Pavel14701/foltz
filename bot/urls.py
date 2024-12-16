from django.urls import path
from .views import TelegramWebhookView

urlpatterns = [
    path('api/BotWebhook', TelegramWebhookView.as_view(), name='telegram_webhook'),
]
