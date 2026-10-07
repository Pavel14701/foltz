from django.core.management.base import BaseCommand

from blog.models import Blog, BlogSection
from blog.seed_data import POSTS


class Command(BaseCommand):
    help = 'Наполняет блог SEO-статьями (идемпотентно: существующие записи обновляются).'

    def handle(self, *args, **options) -> None:
        for data in POSTS:
            post, _ = Blog.objects.update_or_create(
                slug=data['slug'],
                defaults={'title': data['title']},
            )
            for section_data in data['sections']:
                BlogSection.objects.update_or_create(
                    post=post,
                    order=section_data['order'],
                    defaults={
                        key: value
                        for key, value in section_data.items()
                        if key != 'order'
                    },
                )
            self.stdout.write(self.style.SUCCESS(f'OK: {post.title}'))
        self.stdout.write(self.style.SUCCESS(f'Наполнено статей: {len(POSTS)}'))
