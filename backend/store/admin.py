from django.contrib import admin
from .models import ServiceProvider, DataBundle, RouterProduct, Order

@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_editable = ['is_active']

@admin.register(DataBundle)
class DataBundleAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider', 'price', 'data_amount']
    list_filter = ['provider']

@admin.register(RouterProduct)
class RouterProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'service_type', 'status', 'created_at']
    list_filter = ['status', 'service_type']
    list_editable = ['status']