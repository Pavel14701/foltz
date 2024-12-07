import requests
from django.core.mail import send_mail
from .dto import FormData

class SendAplications:
    def __init__(self, form:FormData):
        self.form = form

    def email(self) -> None:
        send_mail(
            'Новая заявка',
            f'Имя: {self.form.name}\nТелефон: {self.form.phone}\nВопрос: {self.form.question}',
            self.form.send_from_email,
            [self.form.send_to_email],
            fail_silently=False,
        )

    def tg(self) -> None:
        telegram_token = self.form.bot_token
        chat_id = self.form.chat_id
        message = f'Имя: {self.form.name}\nТелефон: {self.form.phone}\nВопрос: {self.form.question}'
        requests.post(f'https://api.telegram.org/bot{telegram_token}/sendMessage', data={'chat_id': chat_id, 'text': message})
