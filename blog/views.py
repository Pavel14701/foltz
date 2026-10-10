from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpRequest, HttpResponse

from blog.models import Blog


def blog(request: HttpRequest) -> HttpResponse:
    """Список статей блога: посетителям — только опубликованные."""
    posts = Blog.objects.prefetch_related('blog_section')
    if not request.user.is_staff:
        posts = posts.filter(is_published=True)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """Страница статьи по ЧПУ-slug.

    Неопубликованная статья открывается только staff — это предпросмотр
    черновика перед публикацией.
    """
    post = get_object_or_404(Blog, slug=slug)
    is_preview = False
    if not post.is_published:
        if not request.user.is_staff:
            raise Http404("Статья не найдена")
        is_preview = True
    return render(
        request,
        'blog/post_details.html',
        {'post': post, 'is_preview': is_preview},
    )
