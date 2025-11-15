# store/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet, basename='order')
router.register(r'admin/orders', views.AdminOrderViewSet, basename='admin-order')
router.register(r'providers', views.ServiceProviderViewSet, basename='provider')
router.register(r'admin/providers', views.AdminServiceProviderViewSet, basename='admin-provider')
router.register(r'bundles', views.DataBundleViewSet, basename='bundle')
router.register(r'admin/bundles', views.AdminDataBundleViewSet, basename='admin-bundle')
router.register(r'routers', views.RouterProductViewSet, basename='router')
router.register(r'admin/routers', views.AdminRouterProductViewSet, basename='admin-router')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/status/', views.api_status, name='api-status'),
    path('api/all-services/', views.all_services, name='all-services'),
    path('api/public/providers/', views.public_providers, name='public-providers'),
    path('api/public/bundles/', views.public_bundles, name='public-bundles'),
    path('api/public/routers/', views.public_routers, name='public-routers'),
    path('api/providers/<int:provider_id>/bundles/', views.provider_bundles, name='provider-bundles'),
    path('api/create-order/', views.create_order, name='create-order'),
    path('api/current-user/', views.current_user, name='current-user'),
]