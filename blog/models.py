import re
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category_posts', kwargs={'slug': self.slug})

    def get_post_count(self):
        return self.posts.filter(status='published').count()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:tag_posts', kwargs={'slug': self.slug})

    def get_post_count(self):
        return self.posts.filter(status='published').count()


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=270, unique=True, blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    body = RichTextUploadingField()
    excerpt = models.TextField(
        max_length=500,
        blank=True,
        help_text='Short description shown in post cards. Auto-generated if left blank.',
    )
    featured_image = models.ImageField(
        upload_to='featured_images/%Y/%m/',
        blank=True,
        null=True,
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate unique slug
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug

        # Auto-generate excerpt from body if blank
        if not self.excerpt and self.body:
            clean_body = re.sub(r'<[^>]+>', '', self.body)
            self.excerpt = clean_body[:300] + '...' if len(clean_body) > 300 else clean_body

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def increment_views(self):
        Post.objects.filter(pk=self.pk).update(views_count=models.F('views_count') + 1)
        self.refresh_from_db(fields=['views_count'])

    def get_related_posts(self, count=3):
        related = Post.objects.filter(status='published').exclude(pk=self.pk)
        if self.category:
            by_category = related.filter(category=self.category)
            if by_category.count() >= count:
                return by_category[:count]
        if self.tags.exists():
            by_tags = related.filter(tags__in=self.tags.all()).distinct()
            if by_tags.count() >= count:
                return by_tags[:count]
        return related[:count]

    @property
    def reading_time(self):
        word_count = len(re.sub(r'<[^>]+>', '', self.body).split())
        return max(1, round(word_count / 200))
