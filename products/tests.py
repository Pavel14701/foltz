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

    def test_subtitle_with_content_allowed(self):
        # Новая семантика секций: заголовок и текст можно совмещать.
        section = ProductSection(
            product=self.product, order=1,
            subtitle='Заголовок', content='Текст',
        )
        section.save()  # не должно падать

    def test_image_with_text_rejected(self):
        section = ProductSection(
            product=self.product, order=1,
            subtitle='Заголовок',
            image='x.jpg',
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

    def test_seed_assigns_exchange_fund_category(self):
        self.call_seed()
        from products.models import ProductCategory
        category = ProductCategory.objects.get(slug='obmennyy-fond')
        self.assertEqual(Product.objects.filter(category=category).count(), len(PRODUCTS))


class CatalogPagesTest(TestCase):
    """Страницы каталога: список, поиск, фильтр, карточка товара."""

    def setUp(self):
        from products.models import ProductCategory

        self.amkodor = ProductCategory.objects.create(
            title='Запчасти для техники Амкодор', slug='amkodor', order=10,
        )
        self.mtz = ProductCategory.objects.create(
            title='Запчасти для техники МТЗ', slug='mtz', order=20,
        )
        self.bridge = Product.objects.create(
            title='Мост 342.05.01.000-02', slug='most-342', price='12 000 р.',
            category=self.amkodor, preview_text='Мост в сборе для Амкодор 342.',
        )
        self.engine = Product.objects.create(
            title='ДВС Deutz 1013', slug='dvs-deutz-1013', price='12 800 р.',
            category=self.mtz,
        )

    def test_catalog_lists_products(self):
        response = self.client.get('/tovary/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.bridge.title)
        self.assertContains(response, self.engine.title)
        self.assertContains(response, '12 000 р.')

    def test_catalog_search_filters(self):
        response = self.client.get('/tovary/', {'q': 'Deutz'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.engine.title)
        self.assertNotContains(response, self.bridge.title)

    def test_catalog_category_filter(self):
        response = self.client.get('/tovary/', {'category': 'mtz'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.engine.title)
        self.assertNotContains(response, self.bridge.title)

    def test_catalog_search_and_category_together(self):
        """Поиск и категория работают одновременно (регрессия 500)."""
        response = self.client.get('/tovary/', {'q': 'Deutz', 'category': 'mtz'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.engine.title)
        self.assertNotContains(response, self.bridge.title)
        # Категория без совпадений с запросом — пусто, но не ошибка.
        response = self.client.get('/tovary/', {'q': 'Deutz', 'category': 'amkodor'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.engine.title)

    def test_catalog_partial(self):
        response = self.client.get('/tovary/', {'partial': '1', 'q': 'мост'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.bridge.title)

    def test_product_detail_page(self):
        response = self.client.get('/tovary/most-342/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.bridge.title)
        self.assertContains(response, '12 000 р.')
        # CTA по категории: у Амкодор — услуга ремонта не привязана, но блок есть.
        self.assertContains(response, 'cta-block')
        # Форма заявки с подставленным названием запчасти.
        self.assertContains(response, 'id="request-form"')
        self.assertContains(response, f'Заявка на запчасть: {self.bridge.title}')

    def test_product_detail_404(self):
        response = self.client.get('/tovary/net-takogo/')
        self.assertEqual(response.status_code, 404)


class ProductCategoryCtaTest(TestCase):
    """CTA-блок ремонта подтягивается из категории товара."""

    def setUp(self):
        from products.models import ProductCategory
        from services.models import Service

        self.service = Service.objects.create(
            title='Ремонт техники Амкодор', slug='remont-tehniki-amkodor',
        )
        self.category = ProductCategory.objects.create(
            title='Запчасти Амкодор', slug='zapchasti-amkodor',
            repair_service=self.service,
            cta_title='Нужен ремонт Амкодор?',
            cta_text='Отремонтируем узел.',
        )
        self.product = Product.objects.create(
            title='Коромысло Амкодор 332', slug='koromyslo-332',
            category=self.category,
        )

    def test_cta_uses_category_text_and_service_link(self):
        response = self.client.get('/tovary/koromyslo-332/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Нужен ремонт Амкодор?')
        self.assertContains(response, 'Отремонтируем узел.')
        self.assertContains(response, '/services/remont-tehniki-amkodor/')

    def test_min_price_parses_first_number(self):
        product = Product(title='Ценовой тест', slug='cena-test', price='1900/2300 р.')
        self.assertEqual(product.min_price, 1900)
        product.price = 'договорная'
        self.assertEqual(product.min_price, 0)

