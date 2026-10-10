from django.db import models


class Review(models.Model):
    """Отзыв клиента (контент приходит парсером с volks.by или из админки)."""

    author: str = models.CharField('Автор', max_length=100)
    date = models.DateField('Дата отзыва')
    text = models.TextField('Текст отзыва')

    class Meta:
        ordering = ('-date',)
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        constraints = [
            models.UniqueConstraint(fields=('author', 'date'), name='unique_author_date'),
        ]

    def __str__(self) -> str:
        return f'{self.author} ({self.date:%d.%m.%Y})'
