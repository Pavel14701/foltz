"""Форматирование простого текста секций (блог, услуги) в HTML.

Контент хранится как plain text: \\n — новая строка, пункты списков
начинаются с «- » (маркированный) или «1. » / «1)» (нумерованный).
Фильтр разбивает текст на абзацы <p> и списки <ul>/<ol>, экранируя HTML.
"""

import re

from django import template
from django.utils.html import escape
from django.utils.safestring import SafeString, mark_safe

register = template.Library()

_BULLET_RE = re.compile(r'^[-•*]\s+')
_NUMBERED_RE = re.compile(r'^\d+[.)]\s+')


@register.filter
def richtext(value: str) -> SafeString:
    """Простой текст -> абзацы и списки (с автоэкранированием)."""
    if not value:
        return ''
    blocks: list[str] = []
    list_tag: str | None = None
    items: list[str] = []

    def flush_list() -> None:
        nonlocal list_tag, items
        if items:
            lis = ''.join(f'<li>{item}</li>' for item in items)
            blocks.append(f'<{list_tag}>{lis}</{list_tag}>')
        list_tag, items = None, []

    for raw_line in str(value).splitlines():
        line = raw_line.strip()
        if not line:
            flush_list()
            continue
        if _BULLET_RE.match(line):
            if list_tag != 'ul':
                flush_list()
                list_tag = 'ul'
            items.append(escape(_BULLET_RE.sub('', line)))
        elif (match := _NUMBERED_RE.match(line)):
            if list_tag != 'ol':
                flush_list()
                list_tag = 'ol'
            items.append(escape(line[match.end():]))
        else:
            flush_list()
            blocks.append(f'<p>{escape(line)}</p>')
    flush_list()
    return mark_safe(''.join(blocks))