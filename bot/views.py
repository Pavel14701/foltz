"""Telegram-вебхук для бота."""
import json
import logging

from django.http import HttpRequest, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from bot.bot_instance import bot
from telebot.types import Update

logger = logging.getLogger(__name__)


class TelegramWebhookView(View):
    """Принимает обновления Telegram и передаёт их в бота."""

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        """Обрабатывает одно обновление от Telegram."""
        try:
            data = json.loads(request.body.decode('UTF-8'))
            update = Update.de_json(data)
            bot.process_new_updates([update])
            return JsonResponse({'status': 'ok'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception:
            logger.exception('Error processing update')
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
