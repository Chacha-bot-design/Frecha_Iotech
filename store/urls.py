# store/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # ViewSets
    ElectronicsDevicesViewSet,
    OrderViewSet,
    AdminOrderViewSet,
    ServiceProviderViewSet,
    AdminServiceProviderViewSet,
    DataBundleViewSet,
    AdminDataBundleViewSet,
    RouterProductViewSet,
    AdminRouterProductViewSet,
    
    # Function-based views
    api_status,
    electronics_stats,
    public_electronics,
    public_providers,
    public_bundles,
    public_routers,
    all_services,
    provider_bundles,
    create_order,
    user_login,
    user_logout,
    current_user,
    admin_order_stats,
    admin_update_order_status,
    admin_send_notification,
    admin_search_orders,
    guest_order_signup,
    track_order,
    update_order_tracking,
    
    # Template views
    signup,
    login_view,
    profile,
)

router = DefaultRouter()
router.register(r'electronics', ElectronicsDevicesViewSet, basename='electronics')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'admin/orders', AdminOrderViewSet, basename='admin-orders')
router.register(r'providers', ServiceProviderViewSet, basename='providers')
router.register(r'admin/providers', AdminServiceProviderViewSet, basename='admin-providers')
router.register(r'bundles', DataBundleViewSet, basename='bundles')
router.register(r'admin/bundles', AdminDataBundleViewSet, basename='admin-bundles')
router.register(r'routers', RouterProductViewSet, basename='routers')
router.register(r'admin/routers', AdminRouterProductViewSet, basename='admin-routers')

urlpatterns = [
    # API Routes
    path('api/', include(router.urls)),
    
    # Public API endpoints
    path('api/status/', api_status, name='api_status'),
    path('api/electronics-stats/', electronics_stats, name='electronics_stats'),
    path('api/public-electronics/', public_electronics, name='public_electronics'),
    path('api/public-providers/', public_providers, name='public_providers'),
    path('api/public-bundles/', public_bundles, name='public_bundles'),
    path('api/public-routers/', public_routers, name='public_routers'),
    path('api/all-services/', all_services, name='all_services'),
    path('api/provider/<int:provider_id>/bundles/', provider_bundles, name='provider_bundles'),
    
    # Order management
    path('api/create-order/', create_order, name='create_order'),
    path('api/track-order/<str:tracking_number>/', track_order, name='track_order'),
    path('api/guest-signup/', guest_order_signup, name='guest_order_signup'),
    
    # Authentication
    path('api/login/', user_login, name='user_login'),
    path('api/logout/', user_logout, name='user_logout'),
    path('api/current-user/', current_user, name='current_user'),
    
    # Admin endpoints
    path('api/admin/order-stats/', admin_order_stats, name='admin_order_stats'),
    path('api/admin/orders/<int:order_id>/update-status/', admin_update_order_status, name='admin_update_order_status'),
    path('api/admin/orders/<int:order_id>/send-notification/', admin_send_notification, name='admin_send_notification'),
    path('api/admin/search-orders/', admin_search_orders, name='admin_search_orders'),
    path('api/admin/orders/<int:order_id>/update-tracking/', update_order_tracking, name='update_order_tracking'),
    
    # Template routes (for Django templates if needed)
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
]