from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models import Count, Q, Avg


class PublishedManager(models.Manager):
    """Custom manager for published posts"""
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class PostQuerySet(models.QuerySet):
    """Custom queryset with advanced filtering methods"""
    def published(self):
        return self.filter(status='published')
    
    def by_category(self, category_slug):
        return self.filter(category__slug=category_slug)
    
    def by_tag(self, tag_slug):
        return self.filter(tags__slug=tag_slug)
    
    def by_author(self, author):
        return self.filter(author=author)
    
    def with_comment_count(self):
        return self.annotate(comment_count=Count('comments'))
    
    def popular(self):
        return self.annotate(comment_count=Count('comments')).order_by('-comment_count', '-created_at')
    
    def recent(self):
        return self.order_by('-created_at')
    
    def search(self, query):
        return self.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_detail', kwargs={'slug': self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag_detail', kwargs={'slug': self.slug})


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date='created_at')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/%Y/%m/%d/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    views = models.PositiveIntegerField(default=0)

    # Default manager
    objects = models.Manager()
    # Custom manager
    published = PublishedManager()
    # Custom queryset
    custom = PostQuerySet.as_manager()

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/%Y/%m/%d/', blank=True, null=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}\'s Profile'

    def get_absolute_url(self):
        return reverse('blog:profile', kwargs={'username': self.user.username})


