from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest
from django.views import View
from telebot.types import Update
from bot.bot_instance import bot
import json

class TelegramWebhookView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs):
        try:
            json_str = request.body.decode('UTF-8')
            data = json.loads(json_str)
            update = Update.de_json(data)
            bot.process_new_updates([update])
            return JsonResponse({'status': 'ok'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f"Error processing update: {e}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)