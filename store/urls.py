# store/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'providers', views.ProviderViewSet, basename='provider')
router.register(r'bundles', views.BundleViewSet, basename='bundle')
router.register(r'routers', views.RouterViewSet, basename='router')

urlpatterns = [
    # Public endpoints
    path('status/', views.api_status, name='api-status'),
    path('auth/login/', views.user_login, name='user-login'),
    
    # Protected endpoints (via router)
    path('', include(router.urls)),
    
    # User management
    path('auth/logout/', views.user_logout, name='user-logout'),
    path('auth/me/', views.current_user, name='current-user'),
    
    # Admin only
    path('admin/stats/', views.admin_stats, name='admin-stats'),
]