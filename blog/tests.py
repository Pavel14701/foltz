"""Тесты блога: slug, meta description, публичные страницы, seed-команда, sitemap."""
from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from blog.models import Blog, BlogSection
from blog.seed_data import POSTS, EXTRA_SECTIONS


class BlogModelTest(TestCase):
    def test_slug_auto_generated_from_russian_title(self):
        post = Blog.objects.create(title='Ремонт гидравлики трактора')
        self.assertEqual(post.slug, 'remont-gidravliki-traktora')

    def test_manual_slug_preserved(self):
        post = Blog.objects.create(title='Заголовок статьи', slug='custom-slug')
        self.assertEqual(post.slug, 'custom-slug')

    def test_meta_description_first_content_section(self):
        post = Blog.objects.create(title='Статья')
        BlogSection.objects.create(post=post, order=1, subtitle='Только заголовок')
        BlogSection.objects.create(post=post, order=2, content='Первый текст')
        BlogSection.objects.create(post=post, order=3, content='Второй текст')
        self.assertEqual(post.meta_description, 'Первый текст')

    def test_meta_description_empty_without_content(self):
        post = Blog.objects.create(title='Статья без текста')
        BlogSection.objects.create(post=post, order=1, subtitle='Только заголовок')
        self.assertEqual(post.meta_description, '')


class BlogViewsTest(TestCase):
    def setUp(self):
        self.post = Blog.objects.create(title='Тестовая статья для страницы')
        BlogSection.objects.create(post=self.post, order=1, content='Текст статьи')

    def test_list_view_public_and_contains_post(self):
        response = self.client.get(reverse('blog:blog'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.slug)

    def test_detail_view_public(self):
        response = self.client.get(
            reverse('blog:post_detail', args=[self.post.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, 'Текст статьи')

    def test_unknown_slug_404(self):
        response = self.client.get('/blog/no-such-post/')
        self.assertEqual(response.status_code, 404)

    def test_api_requires_auth(self):
        response = self.client.get('/blog/api/list/')
        self.assertIn(response.status_code, (401, 403))


class SeedPostsCommandTest(TestCase):
    def test_seed_creates_and_is_idempotent(self):
        for _ in range(2):
            call_command('seed_posts', stdout=StringIO())
        self.assertEqual(Blog.objects.count(), len(POSTS))
        self.assertEqual(
            BlogSection.objects.count(),
            sum(
                len(p['sections']) + len(EXTRA_SECTIONS.get(p['slug'], []))
                for p in POSTS
            ),
        )
        post = Blog.objects.get(slug=POSTS[0]['slug'])
        self.assertEqual(post.title, POSTS[0]['title'])

    def test_sitemap_contains_post(self):
        call_command('seed_posts', stdout=StringIO())
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, POSTS[0]['slug'])

