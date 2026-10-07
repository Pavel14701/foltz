from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse

from blog.models import Blog


def blog(request: HttpRequest) -> HttpResponse:
    """Список статей блога — доступен всем, без авторизации."""
    posts = Blog.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """Страница статьи по ЧПУ-slug."""
    post = get_object_or_404(Blog, slug=slug)
    return render(request, 'blog/post_details.html', {'post': post})
