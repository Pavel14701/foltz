from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest
from django.views import View
import telebot
from common.dto import DtoBotConfigs

configs = DtoBotConfigs()
bot = telebot.TeleBot(configs.bot_token)

class TelegramWebhookView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request:HttpRequest, *args, **kwargs):
        json_str = request.body.decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return JsonResponse({'status': 'ok'}, status=200)
