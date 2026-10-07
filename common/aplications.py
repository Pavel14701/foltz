import html
import logging

from django.core.mail import send_mail

from common.dto import FormData
from common.telegram import send_telegram_message

logger = logging.getLogger(__name__)


class SendAplications:
    """Рассылка заявки с сайта: e-mail + Telegram (группа и круг пользователей)."""

    def __init__(self, form: FormData):
        self.form = form

    def email(self) -> None:
        send_mail(
            'Новая заявка',
            f'Имя: {self.form.name}\nТелефон: {self.form.phone}\nВопрос: {self.form.question}',
            self.form.send_from_email,
            self.form.send_to_email,
            fail_silently=False,
        )

    def tg(self) -> None:
        text = (
            '<b>Новая заявка с сайта</b>\n'
            f'<b>Имя:</b> {html.escape(self.form.name)}\n'
            f'<b>Телефон:</b> {html.escape(self.form.phone)}\n'
            f'<b>Вопрос:</b> {html.escape(self.form.question)}'
        )
        failed = send_telegram_message(text)
        if failed:
            logger.warning('Заявка не доставлена получателям: %s', ', '.join(failed))
