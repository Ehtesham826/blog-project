from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Home/Landing page
    path('', views.home_view, name='home'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('post/create/', views.post_create_view, name='post_create'),  # Must come before slug pattern
    path('post/<slug:slug>/update/', views.post_update_view, name='post_update'),
    path('post/<slug:slug>/delete/', views.post_delete_view, name='post_delete'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('my-posts/', views.my_posts_view, name='my_posts'),
    
    # Category and Tag URLs
    path('category/<slug:slug>/', views.category_detail_view, name='category_detail'),
    path('tag/<slug:slug>/', views.tag_detail_view, name='tag_detail'),
    
    # Profile URLs
    path('profile/update/', views.profile_update_view, name='profile_update'),  # Must come before username pattern
    path('profile/<str:username>/', views.profile_view, name='profile'),
]


