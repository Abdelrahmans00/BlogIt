from django.contrib import admin
from django.urls import path,include
from .views import RegisterView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name = 'logout'),
    path('register/', RegisterView.as_view(),name = 'register'),
]
