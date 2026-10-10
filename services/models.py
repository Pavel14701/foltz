import os
import re
from django.db import models
from django.core.exceptions import ValidationError
from pytils.translit import slugify as translit_slugify
import os
from common.base_models import ObjectBaseModel, SectionsBase

def get_upload_to(instance, filename):
    if isinstance(instance, Service):
        return os.path.join('static', 'services', f'service_{instance.title}', filename)
    elif isinstance(instance, ServiceSection):
        return os.path.join('static', 'services', f'service_{instance.service.id}', 'sections', f'section_{instance.id}', filename)
    return os.path.join('static', 'uploads', filename)


class Service(ObjectBaseModel):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True, null=True)
    preview_image = models.ImageField(upload_to=get_upload_to, blank=True, null=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'услуга'
        verbose_name_plural = 'услуги'

    def save(self, *args, **kwargs):
        # ЧПУ для SEO: генерируем из заголовка, если slug не задан вручную
        if not self.slug:
            self.slug = translit_slugify(self.title)
        super().save(*args, **kwargs)

    # Строки, не показываемые в плашке «от N р.»: выезд, договорные работы.
    _SKIP_PRICE_RE = re.compile(r'выезд|/км|договор', re.IGNORECASE)

    def _priceable_rows(self):
        """Позиции прайса с конкретной ценой (для плашек «от N р.»)."""
        return [
            p for p in self.prices.all()
            if not self._SKIP_PRICE_RE.search(p.name)
            and not self._SKIP_PRICE_RE.search(p.price)
            and int(re.sub(r'\D', '', p.price) or 0) > 0
        ]

    @property
    def min_price(self) -> int:
        """Минимальная конкретная цена прайса числом — для плашек «от N р.»."""
        return min(
            (int(re.sub(r'\D', '', p.price) or 0) for p in self._priceable_rows()),
            default=0,
        )

    @property
    def main_price(self) -> str:
        """Цена для карточки: одна позиция — своя цена, несколько — «от N р.»."""
        prices = self._priceable_rows()
        if not prices:
            return ''
        if len(prices) == 1:
            return prices[0].price
        return f'от {self.min_price} р.'


class ServicePrice(models.Model):
    """Позиция прайса услуги (цены хранятся строкой: «от 2500 р.», «600 / 660 р.»)."""

    service = models.ForeignKey(
        'Service',
        related_name='prices',
        on_delete=models.CASCADE,
    )
    name = models.CharField('работа', max_length=255)
    price = models.CharField('цена', max_length=100)

    class Meta:
        ordering = ['id']
        verbose_name = 'позиция прайса'
        verbose_name_plural = 'позиции прайса'
        constraints = [
            models.UniqueConstraint(
                fields=['service', 'name'],
                name='unique_service_price_name',
            ),
        ]

    def __str__(self) -> str:
        return f'{self.service.title}: {self.name} — {self.price}'


class ServiceSection(SectionsBase):
    service = models.ForeignKey('Service', related_name='service_section', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_to, blank=True, null=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'секция услуги'
        verbose_name_plural = 'секции услуг'

    def __str__(self):
        return f"{self.service.title} - {self.order}"

    @property
    def embed_url(self) -> str:
        """YouTube-ссылка, пригодная для вставки в iframe."""
        if self.youtube_url and 'watch?v=' in self.youtube_url:
            return self.youtube_url.replace('watch?v=', 'embed/')
        return self.youtube_url or ''

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)