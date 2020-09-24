"""capital URL Configuration

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
from .views import homePage, faq, referral, tos
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homePage, name="home-page" ),
    path('faq', faq, name='faq'),
    path('terms', tos, name='terms'),
    path('dashboard/', include('dashboard.urls')),
    path('auth/', include('authentication.urls')),
    path('account', include('account.urls')),
    path('referral', referral, name='referral'),
    path('testimony', include('testimony.urls')),
    path('support', include('support.urls')),

    #PASSWORD RESET URLS
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='auth/password/reset_password.html'), name='reset_view'),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password/password_reset_done.html'), name='password_reset_done'),
    path('reset_password_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password/password_reset_complete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)