"""Тесты услуг: slug, секции (embed_url, ограничение «одно поле»), страницы."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from services.models import Service, ServiceSection


class ServiceModelTest(TestCase):
    def test_slug_auto_generated_from_russian_title(self):
        service = Service.objects.create(title='Ремонт гидронасосов')
        self.assertEqual(service.slug, 'remont-gidronasosov')

    def test_manual_slug_preserved(self):
        service = Service.objects.create(title='Диагностика', slug='custom')
        self.assertEqual(service.slug, 'custom')


class ServiceSectionTest(TestCase):
    def setUp(self):
        self.service = Service.objects.create(title='Услуга для секций')

    def test_embed_url_from_watch_link(self):
        section = ServiceSection.objects.create(
            service=self.service,
            order=1,
            youtube_url='https://www.youtube.com/watch?v=abc123',
        )
        self.assertEqual(section.embed_url, 'https://www.youtube.com/embed/abc123')

    def test_embed_url_passthrough(self):
        section = ServiceSection.objects.create(
            service=self.service,
            order=1,
            content='Просто текст',
        )
        self.assertEqual(section.embed_url, '')

    def test_subtitle_with_content_allowed(self):
        # Новая семантика секций: заголовок и текст можно совмещать.
        section = ServiceSection(
            service=self.service, order=1,
            subtitle='Заголовок', content='Текст',
        )
        section.save()  # не должно падать

    def test_image_with_text_rejected(self):
        section = ServiceSection(
            service=self.service, order=1,
            subtitle='Заголовок',
            image='x.jpg',
        )
        with self.assertRaises(ValidationError):
            section.save()

    def test_empty_section_rejected(self):
        section = ServiceSection(service=self.service, order=1)
        with self.assertRaises(ValidationError):
            section.save()


class ServiceViewsTest(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            title='Капитальный ремонт двигателя',
            preview_text='Ремонт Д-240, Д-245',
        )

    def test_list_view_contains_service(self):
        response = self.client.get(reverse('services:services'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.service.title)

    def test_detail_view_public(self):
        response = self.client.get(
            reverse('services:service_detail', args=[self.service.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.service.title)

    def test_unknown_slug_404(self):
        response = self.client.get('/services/no-such-service/')
        self.assertEqual(response.status_code, 404)

from django.test import TestCase

# Create your tests here.
