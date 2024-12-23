from django.core.management.base import BaseCommand
from bot.bot_instance import bot, configs
from bot.handlers import send_welcome, fetch_messages, handle_group_messages

class Command(BaseCommand):
    help = 'Run the Telegram bot with setting webhook or use infinity polling'

    def handle(self, *args, **kwargs) -> None:
        # Регистрация обработчика для команды 'start' и 'help'
        bot.add_message_handler({
            'function': send_welcome,
            'filters': {
                'commands': ['start', 'help']
            }
        })
        # Регистрация обработчика для команды 'messages'
        bot.add_message_handler({
            'function': fetch_messages,
            'filters': {
                'commands': ['messages']
            }
        })
        # Регистрация обработчика для всех остальных сообщений
        bot.add_message_handler({
            'function': handle_group_messages,
            'filters': {
                'func': lambda message: message.chat.id == configs.supergroup_id
            } 
        })
        if configs.use_webhook:
            # Установка вебхука
            bot.set_webhook(url=configs.bot_webhook)
            self.stdout.write(self.style.SUCCESS('Webhook set.'))
        else:
            # Использование пуллинга
            bot.delete_webhook(drop_pending_updates=False)
            bot.infinity_polling(restart_on_change=True)
