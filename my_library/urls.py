"""
URL configuration for my_library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.views.generic import RedirectView
from book_catalog import views
from django.conf import settings
from django.conf.urls.static import static
from .views import UserDetailView, UserDeleteView, UserUpdateView
from django.contrib.auth.views import PasswordResetConfirmView, PasswordChangeView


urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('book_catalog/', include('book_catalog.urls')),
    path('', RedirectView.as_view(url='/book_catalog/', permanent=True)),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('profile/', views.profile_view, name='user'), 
    path('accounts/profile/', UserDetailView.as_view(), name='user_profile'),
    path('accounts/profile/update', UserUpdateView.as_view(), name='edit_profile'),
    # path('accounts/profile/update', profile, name='edit_profile'),
    path('accounts/profile/delete', UserDeleteView.as_view(), name='delete_profile'),
    path('accounts/profile/change_password', PasswordChangeView.as_view(), name='change_password'),
    # path('accounts/profile/update', UserUpdateView.as_view(), name='edit_profile'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
