from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Blog
from products.models import Product
from services.models import Service


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home', 'about', 'forms:contact', 'blog:blog', 'services:services', 'products:catalog']

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return Service.objects.all()

    def location(self, obj):
        return reverse('services:service_detail', args=[obj.slug])


class PostSitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return Blog.objects.all()

    def location(self, obj):
        return reverse('blog:post_detail', args=[obj.slug])

    def lastmod(self, obj):
        return obj.created_at


class ProductSitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'

    def items(self):
        return Product.objects.filter(slug__isnull=False)

    def location(self, obj):
        return reverse('products:product_detail', args=[obj.slug])

