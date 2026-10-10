"""Парсер отзывов с volks.by/news/index.php (блок #sidebar_otzyv).

Структура донора:
    <div id="sidebar_otzyv">
      <div class="text">
        <div class="name_date"><span class="name">Иван</span><span class="date">13.03.2024</span></div>
        <p>Текст отзыва</p>   <!-- закрывающий </p> у донора бывает пропущен -->
      </div>
    </div>
"""
import html
import re
import urllib.request
from datetime import date as date_cls

DONOR_URL = 'https://volks.by/news/index.php'

_REVIEW_RE = re.compile(
    r'<span class="name">(?P<author>[^<]+)</span>'
    r'<span class="date">(?P<date>[^<]+)</span></div>'
    r'<p>(?P<text>.*?)(?:</p>|\s*</div>)',
    re.S,
)
_WS_RE = re.compile(r'\s+')


def fetch_html(url: str = DONOR_URL) -> str:
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (foltz parser)'})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode('utf-8')


def parse_reviews_html(html_source: str) -> list[dict]:
    """Сырой HTML донора -> список словарей {author, date, text} (в порядке появления)."""
    result: list[dict] = []
    for match in _REVIEW_RE.finditer(html_source):
        raw_date = match.group('date').strip()
        text = html.unescape(_WS_RE.sub(' ', match.group('text'))).strip()
        result.append({
            'author': html.unescape(match.group('author').strip()),
            'date': date_cls(*(int(part) for part in reversed(raw_date.split('.')))),
            'text': text,
        })
    return result
