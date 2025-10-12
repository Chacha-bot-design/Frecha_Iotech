# store/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'bundles', views.BundleViewSet, basename='bundle')
router.register(r'providers', views.ProviderViewSet, basename='provider')
router.register(r'routers', views.RouterViewSet, basename='router')

urlpatterns = [
    path('status/', views.api_status, name='api-status'),
    path('auth/login/', views.user_login, name='user-login'),
    
    # Include the router URLs
    path('', include(router.urls)),
]