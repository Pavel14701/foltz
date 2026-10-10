"""Тесты отзывов: модель, парсер, команда, блоки на главной и «О нас»."""
from datetime import date
from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.test import TestCase

from reviews.models import Review
from reviews.parser import parse_reviews_html

_SAMPLE_HTML = '''
<div id="sidebar_otzyv">
  <div id="bx_1"><div class="text">
    <div class="name_date"><span class="name">Иван</span><span class="date">13.03.2024</span></div><p>Отличный ремонт Амкодор 342С.</p>
  </div></div>
  <div id="bx_2"><div class="text">
    <div class="name_date"><span class="name">Петрович</span><span class="date">10.05.2023</span></div><p>Сделали капитальный ремонт двигателя JCB.
  </div></div>
</div>
'''


class ReviewModelTest(TestCase):
    def test_str(self):
        review = Review.objects.create(author='Иван', date=date(2024, 3, 13), text='Текст')
        self.assertEqual(str(review), 'Иван (13.03.2024)')

    def test_ordering_by_date_desc(self):
        Review.objects.create(author='Старый', date=date(2021, 5, 13), text='1')
        Review.objects.create(author='Новый', date=date(2024, 3, 13), text='2')
        self.assertEqual(list(Review.objects.values_list('author', flat=True)), ['Новый', 'Старый'])

    def test_unique_author_date(self):
        Review.objects.create(author='Иван', date=date(2024, 3, 13), text='1')
        with self.assertRaises(Exception):
            Review.objects.create(author='Иван', date=date(2024, 3, 13), text='2')


class ParserTest(TestCase):
    def test_parse_reviews_html(self):
        parsed = parse_reviews_html(_SAMPLE_HTML)
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0]['author'], 'Иван')
        self.assertEqual(parsed[0]['date'], date(2024, 3, 13))
        self.assertEqual(parsed[0]['text'], 'Отличный ремонт Амкодор 342С.')

    def test_parse_handles_missing_closing_p(self):
        parsed = parse_reviews_html(_SAMPLE_HTML)
        self.assertEqual(parsed[1]['author'], 'Петрович')
        self.assertTrue(parsed[1]['text'].startswith('Сделали капитальный'))


class ParseReviewsCommandTest(TestCase):
    def test_command_creates_and_is_idempotent(self):
        with mock.patch('reviews.management.commands.parse_reviews.fetch_html',
                        return_value=_SAMPLE_HTML) as mocked:
            out = StringIO()
            call_command('parse_reviews', stdout=out)
            self.assertIn('Спарсено отзывов: 2, новых: 2', out.getvalue())
            self.assertEqual(Review.objects.count(), 2)
            self.assertEqual(mocked.call_count, 1)

            call_command('parse_reviews', stdout=StringIO())
            self.assertEqual(Review.objects.count(), 2)  # идемпотентно
            self.assertEqual(mocked.call_count, 2)
            self.assertEqual(Review.objects.get(author='Иван').text, 'Отличный ремонт Амкодор 342С.')


class ReviewsPagesTest(TestCase):
    def test_home_shows_latest_reviews(self):
        Review.objects.create(author='Иван', date=date(2024, 3, 13), text='Отлично!')
        response = self.client.get('/')
        self.assertContains(response, 'Отзывы о нас')
        self.assertContains(response, 'Иван')

    def test_about_shows_all_reviews(self):
        Review.objects.create(author='Иван', date=date(2024, 3, 13), text='Первый')
        Review.objects.create(author='Максим', date=date(2021, 5, 13), text='Второй')
        response = self.client.get('/about/')
        self.assertContains(response, 'Иван')
        self.assertContains(response, 'Максим')
