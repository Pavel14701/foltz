from django.core.management.base import BaseCommand

from services.models import Service, ServicePrice, ServiceSection
from services.seed_data import SERVICES


class Command(BaseCommand):
    help = 'Наполняет каталог услуг (идемпотентно: существующие записи обновляются).'

    def handle(self, *args, **options) -> None:
        for data in SERVICES:
            service, _ = Service.objects.update_or_create(
                slug=data['slug'],
                defaults={
                    'title': data['title'],
                    'preview_text': data['preview_text'],
                },
            )
            for section_data in data['sections']:
                ServiceSection.objects.update_or_create(
                    service=service,
                    order=section_data['order'],
                    defaults={
                        key: value
                        for key, value in section_data.items()
                        if key != 'order'
                    },
                )
            # Прайс синхронизируем: создаём/обновляем и удаляем устаревшие позиции
            price_names = []
            for name, price in data.get('prices', []):
                ServicePrice.objects.update_or_create(
                    service=service,
                    name=name,
                    defaults={'price': price},
                )
                price_names.append(name)
            service.prices.exclude(name__in=price_names).delete()
            self.stdout.write(self.style.SUCCESS(f'OK: {service.title}'))
        # Убираем услуги, которых больше нет в каталоге (созданы руками или
        # остались от старой структуры).
        seed_slugs = {data['slug'] for data in SERVICES}
        removed = Service.objects.exclude(slug__in=seed_slugs)
        for service in removed:
            self.stdout.write(self.style.WARNING(f'Удалена: {service.title}'))
        removed.delete()
        self.stdout.write(self.style.SUCCESS(f'Наполнено услуг: {len(SERVICES)}'))