from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']

    def post_count(self, obj):
        count = obj.posts.filter(status='published').count()
        return format_html(
            '<span style="background:#e0e7ff;color:#3730a3;padding:2px 10px;border-radius:12px;font-size:12px;font-weight:600;">{}</span>',
            count
        )
    post_count.short_description = 'Published Posts'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']

    def post_count(self, obj):
        count = obj.posts.filter(status='published').count()
        return format_html(
            '<span style="background:#dcfce7;color:#166534;padding:2px 10px;border-radius:12px;font-size:12px;font-weight:600;">{}</span>',
            count
        )
    post_count.short_description = 'Published Posts'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status_badge', 'views_count', 'created_at', 'featured_image_thumb']
    list_filter = ['status', 'category', 'tags', 'created_at', 'author']
    search_fields = ['title', 'body', 'excerpt', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    filter_horizontal = ['tags']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = ['views_count', 'created_at', 'updated_at']

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'body', 'excerpt'),
        }),
        ('Media', {
            'fields': ('featured_image',),
        }),
        ('Metadata', {
            'fields': ('author', 'category', 'tags', 'status'),
        }),
        ('Statistics', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def status_badge(self, obj):
        if obj.status == 'published':
            return format_html(
                '<span style="background:#dcfce7;color:#166534;padding:2px 10px;border-radius:12px;font-size:12px;font-weight:600;">Published</span>'
            )
        return format_html(
            '<span style="background:#fef9c3;color:#854d0e;padding:2px 10px;border-radius:12px;font-size:12px;font-weight:600;">Draft</span>'
        )
    status_badge.short_description = 'Status'

    def featured_image_thumb(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="width:60px;height:40px;object-fit:cover;border-radius:4px;" />',
                obj.featured_image.url
            )
        return format_html('<span style="color:#9ca3af;font-size:12px;">No image</span>')
    featured_image_thumb.short_description = 'Image'
