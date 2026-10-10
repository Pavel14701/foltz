"""Блок отзывов для главной и «О нас»: {% load reviews_tags %} {% reviews_block 3 %}."""
from django import template

from reviews.models import Review

register = template.Library()


@register.inclusion_tag('reviews/_reviews_block.html')
def reviews_block(limit: int = 3):
    """limit=0 -> показать все отзывы, иначе — первые N (по дате убыв.)."""
    queryset = Review.objects.all() if not limit else Review.objects.all()[:limit]
    return {'reviews': queryset}
