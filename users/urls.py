# users/urls.py
from . import views
from django.urls import include, path

urlpatterns = [
    path('accounts/', include("django.contrib.auth.urls")),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('register/',views.register,name='register'),
]