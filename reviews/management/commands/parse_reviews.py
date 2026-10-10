"""Наполняет отзывы данными с volks.by/news/index.php (идемпотентно)."""
from django.core.management.base import BaseCommand

from reviews.models import Review
from reviews.parser import fetch_html, parse_reviews_html


class Command(BaseCommand):
    help = 'Парсит отзывы с volks.by/news/index.php (update_or_create по автору и дате).'

    def handle(self, *args, **options) -> None:
        parsed = parse_reviews_html(fetch_html())
        created_count = 0
        for item in parsed:
            _, created = Review.objects.update_or_create(
                author=item['author'],
                date=item['date'],
                defaults={'text': item['text']},
            )
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(
            f'Спарсено отзывов: {len(parsed)}, новых: {created_count}.'
        ))
