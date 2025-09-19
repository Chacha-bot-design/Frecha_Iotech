# store/api_urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('providers/', views.api_providers, name='api_providers'),
    path('bundles/', views.api_bundles, name='api_bundles'),
    path('bundles/<int:provider_id>/', views.api_bundles_by_provider, name='api_bundles_by_provider'),
    path('routers/', views.api_routers, name='api_routers'),
    path('orders/', views.api_orders, name='api_orders'),
]