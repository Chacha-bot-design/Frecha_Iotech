from django.contrib import admin
from .models import (
    ServiceProvider, RouterProduct, DataPlan, Bundle, 
    ElectronicsDevices, Order, OrderTracking
)

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'customer_name', 'customer_email', 'customer_phone', 
        'service_type', 'status', 'total_price', 'created_at', 
        'customer_notified'
    ]
    list_filter = ['status', 'service_type', 'customer_notified', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'customer_phone', 'product_details']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
    actions = [
        'mark_as_pending', 'mark_as_confirmed', 'mark_as_processing', 
        'mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled',
        'send_notification_email', 'send_custom_notification'
    ]
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Order Details', {
            'fields': ('service_type', 'product_details', 'quantity', 'total_price', 'notes')
        }),
        ('Order Status & Tracking', {
            'fields': ('status', 'admin_notes', 'tracking_number')
        }),
        ('Notifications', {
            'fields': ('customer_notified', 'notification_sent_at', 'notification_method')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Status actions
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, f"{updated} orders marked as pending")
    mark_as_pending.short_description = "Mark selected orders as pending"
    
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f"{updated} orders marked as confirmed")
    mark_as_confirmed.short_description = "Mark selected orders as confirmed"
    
    def mark_as_processing(self, request, queryset):
        updated = queryset.update(status='processing')
        self.message_user(request, f"{updated} orders marked as processing")
    mark_as_processing.short_description = "Mark selected orders as processing"
    
    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f"{updated} orders marked as shipped")
    mark_as_shipped.short_description = "Mark selected orders as shipped"
    
    def mark_as_delivered(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='delivered', completed_at=timezone.now())
        self.message_user(request, f"{updated} orders marked as delivered")
    mark_as_delivered.short_description = "Mark selected orders as delivered"
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f"{updated} orders marked as cancelled")
    mark_as_cancelled.short_description = "Mark selected orders as cancelled"
    
    # Notification actions
    def send_notification_email(self, request, queryset):
        success_count = 0
        for order in queryset:
            try:
                # Send email notification
                send_mail(
                    f'Order #{order.id} Update - Frecha Iotech',
                    f"""
                    Dear {order.customer_name},
                    
                    Your order #{order.id} is currently being processed.
                    
                    Order Details:
                    - Order ID: #{order.id}
                    - Service: {order.get_service_type_display()}
                    - Product: {order.product_details}
                    - Status: {order.get_status_display()}
                    - Total: TZS {order.total_price}
                    
                    We will notify you once your order is completed.
                    
                    Thank you for choosing Frecha Iotech!
                    
                    Best regards,
                    Frecha Iotech Team
                    """,
                    settings.DEFAULT_FROM_EMAIL,
                    [order.customer_email],
                    fail_silently=False,
                )
                # Update notification status
                order.customer_notified = True
                order.notification_method = 'email'
                order.save()
                success_count += 1
            except Exception as e:
                self.message_user(request, f"Failed to send notification for order #{order.id}: {str(e)}", level='ERROR')
        
        self.message_user(request, f"Email notifications sent for {success_count} orders")
    send_notification_email.short_description = "Send email notification for selected orders"
    
    def send_custom_notification(self, request, queryset):
        # This would typically open a custom admin page for message input
        # For now, we'll use a simple message
        for order in queryset:
            try:
                order.send_notification(
                    method='email', 
                    message="We're processing your order. You'll receive updates soon!"
                )
            except Exception as e:
                self.message_user(request, f"Failed to send notification for order #{order.id}: {str(e)}", level='ERROR')
        
        self.message_user(request, f"Custom notifications sent for {queryset.count()} orders")
    send_custom_notification.short_description = "Send custom notification to selected orders"

@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

@admin.register(RouterProduct)
class RouterProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_available', 'created_at']
    list_filter = ['is_available', 'created_at']
    search_fields = ['name', 'description', 'specifications']
    list_editable = ['price', 'is_available']
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'specifications', 'image')
        }),
        ('Availability', {
            'fields': ('is_available',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

@admin.register(DataPlan)
class DataPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider', 'data_volume', 'validity_days', 'price', 'data_type', 'is_active']
    list_filter = ['provider', 'data_type', 'network_type', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'data_volume']
    list_editable = ['price', 'is_active']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Bundle)
class BundleAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider', 'bundle_type', 'total_data_volume', 'total_price', 'discount_percentage', 'is_featured', 'is_active']
    list_filter = ['provider', 'bundle_type', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'total_data_volume']
    list_editable = ['total_price', 'discount_percentage', 'is_featured', 'is_active']
    filter_horizontal = ['data_plans']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ElectronicsDevices)
class ElectronicsDevicesAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_quantity', 'is_available', 'created_at']
    list_filter = ['category', 'is_available', 'created_at']
    search_fields = ['name', 'description', 'specifications']
    list_editable = ['price', 'stock_quantity', 'is_available']
    readonly_fields = ['created_at', 'updated_at']


# Register the admin classes
admin.site.register(Order, OrderAdmin)

# Optional: Customize admin site header and title
admin.site.site_header = "Frecha Iotech Administration"
admin.site.site_title = "Frecha Iotech Admin"
admin.site.index_title = "Welcome to Frecha Iotech Admin Portal"