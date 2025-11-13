# store/admin.py - ADMIN CODE ONLY
from django.contrib import admin
from .models import ServiceProvider, DataBundle, RouterProduct, Order

@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']

@admin.register(DataBundle)
class DataBundleAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider', 'price', 'data_amount']
    list_filter = ['provider']
    search_fields = ['name']

@admin.register(RouterProduct)
class RouterProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    search_fields = ['name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'service_type', 'status', 'created_at']
    list_filter = ['service_type', 'status', 'created_at']
    search_fields = ['customer_name', 'email']
    readonly_fields = ['created_at']