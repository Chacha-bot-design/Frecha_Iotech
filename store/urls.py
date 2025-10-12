# store/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Protected routes (require login)
protected_router = DefaultRouter()
protected_router.register(r'providers', views.ProtectedProviderViewSet, basename='protected-provider')
protected_router.register(r'bundles', views.ProtectedBundleViewSet, basename='protected-bundle')
protected_router.register(r'routers', views.ProtectedRouterViewSet, basename='protected-router')

urlpatterns = [
    # ============ PUBLIC ROUTES (Anyone can access) ============
    path('public/status/', views.api_status, name='api-status'),
    path('public/providers/', views.public_providers, name='public-providers'),
    path('public/bundles/', views.public_bundles, name='public-bundles'),
    path('public/routers/', views.public_routers, name='public-routers'),
    path('public/contact/', views.public_contact, name='public-contact'),
    
    # ============ TEMPORARY: OLD URLS FOR COMPATIBILITY ============
    path('providers/', views.public_providers, name='old-providers'),
    path('bundles/', views.public_bundles, name='old-bundles'),
    path('routers/', views.public_routers, name='old-routers'),
    
    # ============ AUTHENTICATION ROUTES ============
    path('auth/login/', views.user_login, name='user-login'),
    path('auth/logout/', views.user_logout, name='user-logout'),
    path('auth/me/', views.current_user, name='current-user'),
    
    # ============ PROTECTED ROUTES (Require login) ============
    path('protected/', include(protected_router.urls)),
]