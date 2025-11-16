# store/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router
router = DefaultRouter()

# Register viewsets
router.register(r'providers', views.ServiceProviderViewSet, basename='provider')
router.register(r'bundles', views.DataBundleViewSet, basename='bundle')
router.register(r'routers', views.RouterProductViewSet, basename='router')
router.register(r'orders', views.OrderViewSet, basename='order')

# Admin viewsets
router.register(r'admin/providers', views.AdminServiceProviderViewSet, basename='admin-provider')
router.register(r'admin/bundles', views.AdminDataBundleViewSet, basename='admin-bundle')
router.register(r'admin/routers', views.AdminRouterProductViewSet, basename='admin-router')
router.register(r'admin/orders', views.AdminOrderViewSet, basename='admin-order')

urlpatterns = [
    # Include all router URLs under /api/
    path('api/', include(router.urls)),
    
    # ========== PUBLIC ENDPOINTS ==========
    
    # Service endpoints
    path('api/public/providers/', views.public_providers, name='public-providers'),
    path('api/public/bundles/', views.public_bundles, name='public-bundles'),
    path('api/public/routers/', views.public_routers, name='public-routers'),
    path('api/all-services/', views.all_services, name='all-services'),
    
    # Order endpoints
    path('api/orders/create/', views.create_order, name='create-order'),
    
    # Provider-specific endpoints
    path('api/providers/<int:provider_id>/bundles/', views.provider_bundles, name='provider-bundles'),
    
    # User endpoints
    path('api/current-user/', views.current_user, name='current-user'),
    
    # ========== UTILITY ENDPOINTS ==========
    
    path('api/status/', views.api_status, name='api-status'),
    
    # ========== AUTH ENDPOINTS ==========
    
    path('api/auth/login/', views.user_login, name='user-login'),
    path('api/auth/logout/', views.user_logout, name='user-logout'),
]