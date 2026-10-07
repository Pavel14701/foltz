from django.core.management.base import BaseCommand

from services.models import Service, ServiceSection
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
            self.stdout.write(self.style.SUCCESS(f'OK: {service.title}'))
        self.stdout.write(self.style.SUCCESS(f'Наполнено услуг: {len(SERVICES)}'))