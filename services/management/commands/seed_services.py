import os
import shutil

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand

from services.models import Service, ServicePrice, ServiceSection, ServiceSectionImage
from services.seed_data import SERVICES

IMAGES_DIR = os.path.join(settings.BASE_DIR, 'static', 'images')

# Реальные фото проекта, подобранные по темам услуг (порядок = порядок в галерее).
_THEME_IMAGES = {
    'nasos': ['pult_gidr', 'raspred_rigalet', 'korobka_amk'],
    'motor': ['engine_perkins1', 'engine_jcb1', 'engine_perkins2'],
    'dvigatel': ['engine_jcb1', 'engine_jcb2', 'engine_perkins3'],
    'cilynder': ['jcb_pogr', 'manitoo_pogr', 'amkodor_pogr_new'],
    'cilindr': ['jcb_pogr', 'manitoo_pogr', 'amkodor_pogr_new'],
    'raspredelitel': ['raspred_amk', 'raspred_bosch', 'raspred_mtz_ne_tochno'],
    'korobka': ['korobka_amk', 'korobka_mtz', 'pult_gidr'],
    'gmp': ['korobka_mtz', 'korobka_amk', 'pult_gidr'],
    'kpp': ['korobka_mtz', 'korobka_amk', 'pult_gidr'],
    'transmissiy': ['korobka_amk', 'korobka_mtz', 'pult_gidr'],
    'pogruzchik': ['amkodor_pogr_new', 'manitoo_pogr2', 'jcb_pogr'],
    'amkodor': ['amkodor_pogr_new', 'manitoo_pogr', 'jcb_traktor'],
    'manitoo': ['manitoo_pogr2', 'manitoo_pogr', 'amkodor_pogr_new'],
    'pogr': ['jcb_pogr', 'amkodor_pogr_new', 'manitoo_pogr2'],
    'traktor': ['jcb_traktor', 'traktor_claas_energy', 'kombayn_il'],
    'kombayn': ['kombayn_il', 'traktor_claas_energy', 'jcb_traktor'],
    'gidroraspredelitel': ['raspred_mtz_ne_tochno', 'raspred_rigalet', 'raspred_amk'],
}
# Общий пул для услуг без явной темы.
_FALLBACK_IMAGES = [
    'jcb_traktor', 'traktor_claas_energy', 'kombayn_il', 'man_hero',
    'jcb_pogr', 'amkodor_pogr_new', 'photo_2024-12-06_10-07-21',
]

MEDIA_SEED_DIR = os.path.join(settings.MEDIA_ROOT, 'static', 'services', 'seed')


def _seeded_image(src_name: str) -> SimpleUploadedFile:
    """Копирует реальное фото из static/images в media и возвращает файл для ImageField."""
    src_path = os.path.join(IMAGES_DIR, src_name)
    if not os.path.exists(src_path) and os.path.exists(src_path + '.jpg'):
        src_path += '.jpg'
    dst_dir = MEDIA_SEED_DIR
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, os.path.basename(src_path))
    if not os.path.exists(dst):
        shutil.copyfile(src_path, dst)
    with open(dst, 'rb') as f:
        return SimpleUploadedFile(os.path.basename(dst), f.read(), content_type='image/jpeg')


def _theme_images(service_slug: str, title: str, count: int = 3) -> list[str]:
    """Подбирает реальные фото по теме услуги (ключ в slug/названии), иначе общий пул."""
    low = f'{service_slug} {title}'.lower()
    for key, names in _THEME_IMAGES.items():
        if key in low:
            return names[:count]
    start = sum(ord(ch) for ch in service_slug) % len(_FALLBACK_IMAGES)
    return [_FALLBACK_IMAGES[(start + i) % len(_FALLBACK_IMAGES)] for i in range(count)]


class Command(BaseCommand):
    help = 'Наполняет каталог услуг (идемпотентно: существующие записи обновляются).'

    def handle(self, *args, **options) -> None:
        idx = 0
        for data in SERVICES:
            idx += 1
            service, _ = Service.objects.update_or_create(
                slug=data['slug'],
                defaults={
                    'title': data['title'],
                    'preview_text': data['preview_text'],
                },
            )
            # Реальное фото для hero-блока «картинка + текст».
            hero_img = _seeded_image(_theme_images(data['slug'], data['title'])[0])
            service.preview_image.save(hero_img.name, hero_img, save=False)
            service.save()
            for section_data in data['sections']:
                section, _ = ServiceSection.objects.update_or_create(
                    service=service,
                    order=section_data['order'],
                    defaults={
                        key: value
                        for key, value in section_data.items()
                        if key != 'order'
                    },
                )
                # Галерея (3 реальных фото) на секциях с текстом.
                # Источник истины — сид: пересоздаём галерею с нуля.
                section.gallery.all().delete()
                if section.content:
                    for order, src_name in enumerate(
                        _theme_images(data['slug'], data['title']), start=1,
                    ):
                        ServiceSectionImage.objects.create(
                            section=section,
                            image=_seeded_image(src_name),
                            order=order,
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