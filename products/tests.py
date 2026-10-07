"""Тесты товаров: превью и ограничение секций «ровно одно поле»."""
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase

from products.models import Product, ProductSection
from products.seed_data import PRODUCTS


class ProductTest(TestCase):
    def test_clean_rejects_image_and_video_together(self):
        product = Product(
            title='Товар',
            preview_image='img.jpg',
            preview_video_url='https://youtube.com/watch?v=1',
        )
        with self.assertRaises(ValidationError):
            product.clean()

    def test_clean_allows_only_video(self):
        product = Product(title='Товар', preview_video_url='https://youtube.com/watch?v=1')
        product.clean()  # не должно падать


class ProductSectionTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(title='Товар для секций')

    def test_two_fields_filled_rejected(self):
        section = ProductSection(
            product=self.product, order=1,
            subtitle='Заголовок', content='Текст',
        )
        with self.assertRaises(ValidationError):
            section.save()

    def test_single_field_allowed(self):
        section = ProductSection.objects.create(
            product=self.product, order=1, content='Текст',
        )
        self.assertEqual(str(section), 'Товар для секций - 1')


class SeedProductsTest(TestCase):
    """Сид-команда наполняет каталог идемпотентно."""

    def call_seed(self) -> None:
        call_command('seed_products', verbosity=0)

    def test_creates_products_and_sections(self):
        self.call_seed()
        self.assertEqual(Product.objects.count(), len(PRODUCTS))
        self.assertEqual(
            ProductSection.objects.count(),
            sum(len(p['sections']) for p in PRODUCTS),
        )

    def test_idempotent(self):
        self.call_seed()
        self.call_seed()
        self.assertEqual(Product.objects.count(), len(PRODUCTS))

