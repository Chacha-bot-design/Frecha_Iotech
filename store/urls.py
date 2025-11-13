from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import OrderViewSet, AdminOrderViewSet

# Admin routes (require login)
admin_router = DefaultRouter()
admin_router.register(r'admin/providers', views.AdminServiceProviderViewSet, basename='admin-provider')
admin_router.register(r'admin/bundles', views.AdminDataBundleViewSet, basename='admin-bundle')
admin_router.register(r'admin/routers', views.AdminRouterProductViewSet, basename='admin-router')
admin_router.register(r'admin/orders', views.AdminOrderViewSet, basename='admin-order')

# User order routes
order_router = DefaultRouter()
order_router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    # ============ PUBLIC ROUTES (Anyone can access) ============
    path('public/status/', views.api_status, name='api-status'),
    path('public/providers/', views.public_providers, name='public-providers'),
    path('public/bundles/', views.public_bundles, name='public-bundles'),
    path('public/routers/', views.public_routers, name='public-routers'),
    path('public/orders/create/', views.create_order, name='create-order'),
    path('public/providers/<int:provider_id>/bundles/', views.provider_bundles, name='provider-bundles'),
    
    # ============ TEMPORARY: OLD URLS FOR COMPATIBILITY ============
    path('providers/', views.public_providers, name='old-providers'),
    path('bundles/', views.public_bundles, name='old-bundles'),
    path('routers/', views.public_routers, name='old-routers'),
    path('bundles-by-provider/<int:provider_id>/', views.provider_bundles, name='old-bundles-by-provider'),
    
    # ============ AUTHENTICATION ROUTES ============
    path('auth/login/', views.user_login, name='user-login'),
    path('auth/logout/', views.user_logout, name='user-logout'),
    path('auth/me/', views.current_user, name='current-user'),
    
    # ============ USER ORDER ROUTES (Require login) ============
    path('', include(order_router.urls)),
    
    # ============ ADMIN ROUTES (Require login) ============
    path('', include(admin_router.urls)),
]