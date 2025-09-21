from django.urls import path
from . import views  # Import from the current app's views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('api/providers/', views.api_providers, name='api_providers'),
    path('api/bundles/', views.api_bundles, name='api_bundles'),
    path('api/bundles/<int:provider_id>/', views.api_bundles_by_provider, name='api_bundles_by_provider'),
    path('api/routers/', views.api_routers, name='api_routers'),
    path('api/orders/', views.api_create_order, name='api_create_order'),
]