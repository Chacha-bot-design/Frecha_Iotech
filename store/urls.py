# store/urls.py - ADD THESE LINES
from django.urls import path
from . import views

urlpatterns = [
    # ============ NEW PUBLIC ROUTES ============
    path('public/providers/', views.public_providers, name='public-providers'),
    path('public/bundles/', views.public_bundles, name='public-bundles'),
    path('public/routers/', views.public_routers, name='public-routers'),
    path('public/status/', views.api_status, name='api-status'),
    path('public/contact/', views.public_contact, name='public-contact'),
    
    # ============ TEMPORARY: OLD URLS FOR COMPATIBILITY ============
    path('providers/', views.public_providers, name='old-providers'),
    path('bundles/', views.public_bundles, name='old-bundles'),
    path('routers/', views.public_routers, name='old-routers'),
    
    # ============ AUTHENTICATION ROUTES ============
    path('auth/login/', views.user_login, name='user-login'),
    path('auth/logout/', views.user_logout, name='user-logout'),
    path('auth/me/', views.current_user, name='current-user'),
]