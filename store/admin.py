from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered']
    
    def mark_as_processing(self, request, queryset):
        queryset.update(status='processing')
    mark_as_processing.short_description = "Mark selected orders as Processing"
    
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
    mark_as_shipped.short_description = "Mark selected orders as Shipped"
    
    def mark_as_delivered(self, request, queryset):
        for order in queryset:
            order.mark_completed()
    mark_as_delivered.short_description = "Mark selected orders as Delivered"