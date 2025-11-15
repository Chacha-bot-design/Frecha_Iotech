# store/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Admin routes
admin_router = DefaultRouter()
admin_router.register(r'admin/providers', views.AdminServiceProviderViewSet, basename='admin-provider')
admin_router.register(r'admin/bundles', views.AdminDataBundleViewSet, basename='admin-bundle')
admin_router.register(r'admin/routers', views.AdminRouterProductViewSet, basename='admin-router')
admin_router.register(r'admin/orders', views.AdminOrderViewSet, basename='admin-order')

# User routes  
user_router = DefaultRouter()
user_router.register(r'orders', views.OrderViewSet, basename='orders')
user_router.register(r'products', views.ProductViewSet, basename='products')
user_router.register(r'categories', views.CategoryViewSet, basename='categories')
user_router.register(r'providers', views.ServiceProviderViewSet, basename='providers')
user_router.register(r'bundles', views.DataBundleViewSet, basename='bundles')
user_router.register(r'routers', views.RouterProductViewSet, basename='routers')

urlpatterns = [
    # Public routes
    path('public/status/', views.api_status, name='api-status'),
    path('public/providers/', views.public_providers, name='public-providers'),
    path('public/bundles/', views.public_bundles, name='public-bundles'),
    path('public/routers/', views.public_routers, name='public-routers'),
    path('public/orders/create/', views.create_order, name='create-order'),
    path('public/providers/<int:provider_id>/bundles/', views.provider_bundles, name='provider-bundles'),
    
    # Authentication
    path('auth/login/', views.user_login, name='user-login'),
    path('auth/logout/', views.user_logout, name='user-logout'),
    path('auth/me/', views.current_user, name='current-user'),
    
    # Include routers
    path('', include(user_router.urls)),
    path('', include(admin_router.urls)),
]