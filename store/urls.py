# store/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('status/', views.api_status, name='api-status'),
    path('auth/login/', views.user_login, name='user-login'),
    path('bundles/', views.bundle_list, name='bundle-list'),
    path('providers/', views.provider_list, name='provider-list'),
    path('routers/', views.router_list, name='router-list'),
]