from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.conf import settings
from django.contrib import messages
from .models import Post, Category, Tag
from .forms import PostForm, SearchForm


def get_sidebar_context():
    return {
        'categories': Category.objects.annotate(
            post_count=Count('posts', filter=Q(posts__status='published'))
        ).filter(post_count__gt=0).order_by('-post_count'),
        'tags': Tag.objects.annotate(
            post_count=Count('posts', filter=Q(posts__status='published'))
        ).filter(post_count__gt=0).order_by('-post_count')[:20],
        'recent_posts': Post.objects.filter(status='published').order_by('-created_at')[:5],
    }


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = getattr(settings, 'POSTS_PER_PAGE', 6)

    def get_queryset(self):
        qs = Post.objects.filter(status='published').select_related(
            'author', 'category'
        ).prefetch_related('tags').order_by('-created_at')

        category_slug = self.request.GET.get('category')
        tag_slug = self.request.GET.get('tag')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        if tag_slug:
            qs = qs.filter(tags__slug=tag_slug)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_sidebar_context())
        context['search_form'] = SearchForm()
        context['active_category'] = self.request.GET.get('category')
        context['active_tag'] = self.request.GET.get('tag')
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Post.objects.filter(status='published').select_related(
            'author', 'category'
        ).prefetch_related('tags')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.increment_views()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_sidebar_context())
        context['related_posts'] = self.object.get_related_posts(count=3)
        context['search_form'] = SearchForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create New Post'
        context['submit_label'] = 'Publish Post'
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    slug_url_kwarg = 'slug'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Edit: {self.object.title}'
        context['submit_label'] = 'Save Changes'
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    slug_url_kwarg = 'slug'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, 'Post deleted successfully.')
        return super().form_valid(form)


def search_view(request):
    form = SearchForm(request.GET or None)
    results = []
    query = ''

    if form.is_valid():
        query = form.cleaned_data['query']
        results = Post.objects.filter(status='published').filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(category__name__icontains=query)
        ).select_related('author', 'category').prefetch_related('tags').distinct().order_by('-created_at')

    context = {
        'form': form,
        'results': results,
        'query': query,
        'result_count': results.count() if hasattr(results, 'query') else 0,
        'search_form': form,
    }
    context.update(get_sidebar_context())
    return render(request, 'blog/search_results.html', context)


class TagPostListView(ListView):
    model = Post
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    paginate_by = getattr(settings, 'POSTS_PER_PAGE', 6)

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(
            tags=self.tag, status='published'
        ).select_related('author', 'category').prefetch_related('tags').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context.update(get_sidebar_context())
        context['search_form'] = SearchForm()
        return context


class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = getattr(settings, 'POSTS_PER_PAGE', 6)

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(
            category=self.category, status='published'
        ).select_related('author', 'category').prefetch_related('tags').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context.update(get_sidebar_context())
        context['search_form'] = SearchForm()
        return context
