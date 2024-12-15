from bot.bot_instance import bot, configs
import requests
from telebot.types import Message


class SiteMsgAPI:
    api_url = configs.site_api_url
    def get_messages(self):
        response = requests.get(self.api_url)
        return response.json()

    def send_message_to_site(self, sender, body):
        data = {
            'sender': sender,
            'body': body,
        }
        response = requests.post(self.api_url, json=data)
        return response.json()

    def send_message_to_group(self, sender, subject, body):
        message = f"Сообщение от {sender}:\nТема: {subject}\n{body}"
        bot.send_message(configs.supergroup_id, message)


def send_welcome(message:Message):
    if message.from_user.id in configs.admin_user_ids:
        return bot.reply_to(message, "Welcome Admin! Use comand \"/messages\" to get user messages.")
    bot.reply_to(message, 'Уёбывай ка ты нахуй отсюда, пока пизды не вломили!')

def fetch_messages(message:Message):
    api = SiteMsgAPI()
    if str(message.from_user.id) in configs.admin_user_ids:
        messages = api.get_messages()
        for msg in messages:
            api.send_message_to_group(msg['name'], msg['subject'], msg['body'])

configs.supergroup_id

def handle_group_messages(message:Message):
    api = SiteMsgAPI()
    if message.reply_to_message and str(message.chat.id) in configs.admin_user_ids:
        original_message = message.reply_to_message.text
        # Предполагается, что оригинальное сообщение имеет формат:
        # "Сообщение от {sender}:\nТема: {subject}\n{body}"
        sender_info, subject_info, body_info = original_message.split('\n', 2)
        sender = sender_info.replace("Сообщение от ", "").strip()
        response_body = message.text
        api.send_message_to_site(sender, response_body)
        bot.reply_to(message, "Ответ отправлен на сайт!")
