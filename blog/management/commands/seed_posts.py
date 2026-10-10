import os
import shutil

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand

from blog.models import Blog, BlogSection, BlogSectionImage
from blog.seed_data import CTA_BY_SLUG, DEFAULT_CTA, EXTRA_SECTIONS, GALLERY, POSTS

IMAGES_DIR = os.path.join(settings.BASE_DIR, 'static', 'images')


def seeded_image(src_name: str) -> str:
    """Копирует картинку из static/images в media и возвращает путь для ImageField."""
    dst_dir = os.path.join(settings.MEDIA_ROOT, 'static', 'posts', 'seed')
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, src_name)
    if not os.path.exists(dst):
        shutil.copyfile(os.path.join(IMAGES_DIR, src_name), dst)
    return os.path.join('static', 'posts', 'seed', src_name)


class Command(BaseCommand):
    help = 'Наполняет блог SEO-статьями (идемпотентно: существующие записи обновляются).'

    def handle(self, *args, **options) -> None:
        for data in POSTS:
            cta = {**DEFAULT_CTA, 'position': None, **CTA_BY_SLUG.get(data['slug'], {})}
            post, _ = Blog.objects.update_or_create(
                slug=data['slug'],
                defaults={
                    'title': data['title'],
                    'is_published': True,
                    'show_cta': True,
                    'cta_title': cta['title'],
                    'cta_text': cta['text'],
                    'cta_position': cta['position'],
                },
            )
            sections = list(data['sections']) + list(EXTRA_SECTIONS.get(data['slug'], []))
            # данные секций — источник истины: пересоздаём с нуля (порядок и состав меняются)
            post.blog_section.all().delete()
            sections_objs = {}
            for order, section_data in enumerate(sections, start=1):
                fields = {
                    key: value
                    for key, value in section_data.items()
                    if key not in ('order', 'image_src')
                }
                if section_data.get('image_src'):
                    fields['image'] = seeded_image(section_data['image_src'])
                sections_objs[order] = BlogSection.objects.create(post=post, order=order, **fields)
            # галерея — источник истины тоже данные: пересоздаём с нуля
            post.gallery_images.all().delete()
            for order, (section_ref, src_name) in enumerate(GALLERY.get(data['slug'], []), start=1):
                src_path = os.path.join(IMAGES_DIR, src_name)
                if not os.path.exists(src_path) and os.path.exists(src_path + '.jpg'):
                    src_path += '.jpg'
                img = SimpleUploadedFile(
                    os.path.basename(src_path),
                    open(src_path, 'rb').read(),
                    content_type='image/jpeg',
                )
                BlogSectionImage.objects.create(
                    post=post,
                    section=sections_objs.get(section_ref),
                    image=img,
                    order=order,
                )
            self.stdout.write(self.style.SUCCESS(f'OK: {post.title} ({len(sections)} секций)'))
        self.stdout.write(self.style.SUCCESS(f'Наполнено статей: {len(POSTS)}'))
