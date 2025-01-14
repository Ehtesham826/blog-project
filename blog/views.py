from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Case, When, IntegerField
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment, Category, Tag, UserProfile
from .forms import UserRegistrationForm, PostForm, CommentForm, UserProfileForm


# Authentication Views
def register_view(request):
    if request.user.is_authenticated:
        return redirect('blog:post_list')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created successfully.')
            return redirect('blog:post_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'blog/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('blog:post_list')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'blog/password_reset.html'
    email_template_name = 'blog/password_reset_email.html'
    subject_template_name = 'blog/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'blog/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'blog/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'blog/password_reset_complete.html'


# Blog Views
def home_view(request):
    """Landing page with hero section and features"""
    latest_posts = Post.published.select_related('author', 'category').prefetch_related('tags')[:3]
    return render(request, 'blog/home.html', {'latest_posts': latest_posts})

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.published.all()
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()
        
        # Category filter
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Tag filter
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        
        return queryset.select_related('author', 'category').prefetch_related('tags').annotate(
            comment_count=Count('comments')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all categories with published post count, exclude empty slugs
        # Count only published posts
        context['categories'] = Category.objects.exclude(
            slug=''
        ).exclude(
            slug__isnull=True
        ).annotate(
            post_count=Count(
                Case(
                    When(posts__status='published', then=1),
                    output_field=IntegerField()
                ),
                distinct=True
            )
        ).order_by('name')
        # Get all tags with published post count, exclude empty slugs
        context['tags'] = Tag.objects.exclude(
            slug=''
        ).exclude(
            slug__isnull=True
        ).annotate(
            post_count=Count(
                Case(
                    When(posts__status='published', then=1),
                    output_field=IntegerField()
                ),
                distinct=True
            )
        ).order_by('name')[:10]
        context['popular_posts'] = Post.published.annotate(
            comment_count=Count('comments')
        ).order_by('-comment_count', '-created_at')[:5]
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Post.objects.select_related('author', 'category').prefetch_related('tags', 'comments__author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Increment views
        post.increment_views()
        
        # Get comments
        context['comments'] = post.comments.filter(active=True)
        context['comment_form'] = CommentForm()
        
        # Related posts
        context['related_posts'] = Post.published.filter(
            category=post.category
        ).exclude(id=post.id)[:3]
        
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added successfully!')
            return redirect('blog:post_detail', slug=post.slug)
        
        context = self.get_context_data()
        context['comment_form'] = comment_form
        return render(request, self.template_name, context)


@login_required
def post_create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save many-to-many relationships (tags)
            messages.success(request, 'Post created successfully!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Create Post'})


@login_required
def post_update_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    # Check if user is the author
    if post.author != request.user:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('blog:post_detail', slug=post.slug)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'post': post, 'title': 'Update Post'})


@login_required
def post_delete_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    # Check if user is the author
    if post.author != request.user:
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('blog:post_detail', slug=post.slug)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('blog:post_list')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required
def my_posts_view(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/my_posts.html', {'page_obj': page_obj})


def category_detail_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.published.filter(category=category).select_related('author', 'category').prefetch_related('tags')
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/category_detail.html', {'category': category, 'page_obj': page_obj})


def tag_detail_view(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.published.filter(tags=tag).select_related('author', 'category').prefetch_related('tags')
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/tag_detail.html', {'tag': tag, 'page_obj': page_obj})


# Profile Views
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = UserProfile.objects.get_or_create(user=user)
    posts = Post.published.filter(author=user).order_by('-created_at')[:5]
    return render(request, 'blog/profile.html', {
        'profile_user': user,
        'profile': profile,
        'posts': posts
    })


@login_required
def profile_update_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('blog:profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'blog/profile_update.html', {'form': form})


