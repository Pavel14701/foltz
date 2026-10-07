"""Тесты общих страниц: главная с галереей, статические, get-image-url."""
from django.test import TestCase


class StaticPagesTest(TestCase):
    def test_home_renders_gallery(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ghost-gallery')
        self.assertContains(response, 'need-background-image')

    def test_about(self):
        self.assertEqual(self.client.get('/about/').status_code, 200)


class GetImageUrlTest(TestCase):
    def test_returns_image_url(self):
        response = self.client.get('/get-image-url/amkodor_pogr_new.jpg/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {'image_url': '/static/images/amkodor_pogr_new.jpg'},
        )

    def test_post_not_allowed(self):
        response = self.client.post('/get-image-url/amkodor_pogr_new.jpg/')
        self.assertEqual(response.status_code, 405)
