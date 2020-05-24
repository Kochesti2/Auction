"""Auction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from Auction import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.homeView, name='home'),

    path('about/', views.about_view, name="about_view"),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/password_reset/',auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),name='password_reset'),
    path('accounts/password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
    path('accounts/reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),
    path('accounts/reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),

    path('admin/', admin.site.urls), ]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
# ]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
