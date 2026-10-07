from django.core.management.base import BaseCommand

from products.models import Product, ProductSection
from products.seed_data import PRODUCTS


class Command(BaseCommand):
    help = 'Наполняет каталог продуктов (идемпотентно: существующие записи обновляются).'

    def handle(self, *args, **options) -> None:
        for data in PRODUCTS:
            product, _ = Product.objects.update_or_create(
                title=data['title'],
                defaults={'preview_text': data['preview_text']},
            )
            for section_data in data['sections']:
                ProductSection.objects.update_or_create(
                    product=product,
                    order=section_data['order'],
                    defaults={
                        key: value
                        for key, value in section_data.items()
                        if key != 'order'
                    },
                )
            self.stdout.write(self.style.SUCCESS(f'OK: {product.title}'))
        self.stdout.write(self.style.SUCCESS(f'Наполнено продуктов: {len(PRODUCTS)}'))
