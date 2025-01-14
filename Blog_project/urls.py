"""
URL configuration for Blog_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    
    # Authentication URLs
    path("register/", views.register_view, name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("password-reset/", views.CustomPasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", views.CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", views.CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password-reset-complete/", views.CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
