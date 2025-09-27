from django.contrib import admin
from .models import ServiceProvider, DataBundle, RouterProduct, Order

# Service Provider Admin
@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo', 'color']
    list_editable = ['logo', 'color']
    search_fields = ['name']

# Data Bundle Admin
@admin.register(DataBundle)
class DataBundleAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider', 'price', 'validity']
    list_filter = ['provider']
    search_fields = ['name', 'provider__name']
    list_editable = ['price']

# Router Product Admin
@admin.register(RouterProduct)
class RouterProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    search_fields = ['name']
    list_editable = ['price']

# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'email', 'service_type', 'status', 'created_at']
    list_filter = ['status', 'service_type', 'created_at']
    search_fields = ['customer_name', 'email', 'phone']
    readonly_fields = ['created_at']
    list_editable = ['status']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('created_at',)
        return self.readonly_fields