from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest
from django.views import View
from telebot.types import Update
from bot.bot_instance import bot


class TelegramWebhookView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request:HttpRequest, *args, **kwargs):
        json_str = request.body.decode('UTF-8')
        update = Update.de_json(json_str)
        bot.process_new_updates([update])
        return JsonResponse({'status': 'ok'}, status=200)
