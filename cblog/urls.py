from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from blog.sitemaps import PostSitemap, CategorySitemap, TagSitemap

sitemaps = {
    'posts': PostSitemap,
    'categories': CategorySitemap,
    'tags': TagSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('googleb61f5d167de33ff2.html', TemplateView.as_view(template_name='googleb61f5d167de33ff2.html', content_type='text/html')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('blog.urls', namespace='blog')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
