from django.contrib.sitemaps import Sitemap
from .models import Post, Category, Tag


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.objects.filter(status='published').order_by('-created_at')

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Category.objects.all()


class TagSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.4

    def items(self):
        return Tag.objects.all()
