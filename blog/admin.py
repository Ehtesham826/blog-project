from django.contrib import admin
from .models import Post, Category, Tag, Comment, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'created_at', 'views']
    list_filter = ['status', 'created_at', 'category', 'tags']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'created_at'
    filter_horizontal = ['tags']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at', 'active']
    list_filter = ['active', 'created_at']
    search_fields = ['content', 'author__username', 'post__title']
    raw_id_fields = ['post', 'author']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'created_at']
    search_fields = ['user__username', 'bio', 'location']
    raw_id_fields = ['user']


