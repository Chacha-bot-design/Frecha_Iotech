# store/admin.py
from django.contrib import admin
from .models import ServiceProvider, RouterProduct, DataBundle, Order

@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_email', 'phone_number', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'contact_email']
    list_editable = ['is_active']

@admin.register(RouterProduct)
class RouterProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_available', 'created_at']
    list_filter = ['is_available', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'is_available']

@admin.register(DataBundle)
class DataBundleAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider', 'price', 'data_volume', 'validity_days', 'is_active']
    list_filter = ['provider', 'is_active', 'created_at']
    search_fields = ['name', 'provider__name']
    list_editable = ['price', 'is_active']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_email', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'customer_phone']
    list_editable = ['status']