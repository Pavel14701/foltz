"""Тесты заявок: страница контактов, приём форм, отправка на email и в Telegram."""
from unittest import mock

from django.test import SimpleTestCase


class ContactPageTest(SimpleTestCase):
    """«Контакты» — контактные данные + форма на консультацию."""

    def test_get_renders_contacts_with_consultation_form(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        # Контактные данные (из site_contacts).
        self.assertContains(response, '+375 (44) 577-00-04')
        self.assertContains(response, 'volksagro@gmail.com')
        self.assertContains(response, 'Сухаревская')
        # Форма на консультацию.
        self.assertContains(response, 'name="phone"')
        self.assertContains(response, 'id="request-form"')


class SendRequestTest(SimpleTestCase):
    """Единая точка приёма заявок со страниц товаров и услуг."""

    def test_get_is_not_allowed(self):
        response = self.client.get('/request/')
        self.assertEqual(response.status_code, 405)

    @mock.patch('forms.views.SendAplications')
    def test_valid_post_sends_and_redirects(self, sender_cls):
        response = self.client.post('/request/', {
            'name': 'Иван',
            'phone': '+375291112233',
            'question': 'Сколько стоит ремонт насоса?',
        })
        self.assertRedirects(response, '/success/', fetch_redirect_response=False)
        form_data = sender_cls.call_args[0][0]
        self.assertEqual(form_data.name, 'Иван')
        self.assertEqual(form_data.phone, '+375291112233')
        self.assertEqual(form_data.question, 'Сколько стоит ремонт насоса?')
        sender_cls.return_value.email.assert_called_once()
        sender_cls.return_value.tg.assert_called_once()

    @mock.patch('forms.views.SendAplications')
    def test_invalid_post_rerenders_with_errors(self, sender_cls):
        response = self.client.post('/request/', {'phone': '+375291112233'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.context['form'].errors)
        sender_cls.assert_not_called()

    @mock.patch('forms.views.SendAplications')
    def test_empty_question_is_optional(self, sender_cls):
        response = self.client.post('/request/', {'name': 'Иван', 'phone': '123'})
        self.assertRedirects(response, '/success/', fetch_redirect_response=False)
        self.assertEqual(sender_cls.call_args[0][0].question, '')

from django.test import TestCase

# Create your tests here.
