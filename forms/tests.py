"""Тесты формы обратной связи: валидация и отправка заявок."""
from unittest import mock

from django.test import SimpleTestCase


class ContactViewTest(SimpleTestCase):
    def test_get_renders_form(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="phone"')

    @mock.patch('forms.views.SendAplications')
    def test_valid_post_sends_and_redirects(self, sender_cls):
        response = self.client.post('/contact/', {
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
        response = self.client.post('/contact/', {'phone': '+375291112233'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.context['form'].errors)
        sender_cls.assert_not_called()

    @mock.patch('forms.views.SendAplications')
    def test_empty_question_is_optional(self, sender_cls):
        response = self.client.post('/contact/', {'name': 'Иван', 'phone': '123'})
        self.assertRedirects(response, '/success/', fetch_redirect_response=False)
        self.assertEqual(sender_cls.call_args[0][0].question, '')

from django.test import TestCase

# Create your tests here.
