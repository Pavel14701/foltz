import telebot
from common.dto import DtoBotConfigs


configs = DtoBotConfigs()
bot = telebot.TeleBot(configs.bot_token, threaded=True, num_threads=5)

