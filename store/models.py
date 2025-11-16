# store/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ServiceProvider(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Service Provider"
        verbose_name_plural = "Service Providers"

class RouterProduct(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    specifications = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='routers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class DataBundle(models.Model):
    name = models.CharField(max_length=255)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='bundles')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    data_volume = models.CharField(max_length=50, default='1GB')
    validity_days = models.IntegerField(default=30)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.provider.name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='orders')
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    product_details = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"
    
    def mark_completed(self):
        self.status = 'delivered'
        self.completed_at = timezone.now()
        self.save()
        SERVICE_TYPES = [
        ('bundle', 'Data Bundle'),
        ('router', 'Router Product'),
    ]
    
    # Customer information
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    
    # Order details
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES, default='bundle')
    product_details = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    
    # ✅ ADD THESE NOTIFICATION FIELDS
    customer_notified = models.BooleanField(default=False)
    notification_sent_at = models.DateTimeField(null=True, blank=True)
    notification_method = models.CharField(
        max_length=20, 
        choices=[('email', 'Email'), ('sms', 'SMS'), ('both', 'Both')],
        blank=True, 
        null=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Order"
        verbose_name_plural = "Orders"
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name} - {self.get_status_display()}"
    
    def mark_completed(self):
        self.status = 'delivered'
        self.completed_at = timezone.now()
        self.save()
    
    # ✅ ADD THIS NOTIFICATION METHOD
    def send_notification(self, method='email', message=None):
        """Send notification to customer"""
        from django.core.mail import send_mail
        from django.conf import settings
        
        if not message:
            message = f"Your order #{self.id} status has been updated to: {self.get_status_display()}"
        
        try:
            if method in ['email', 'both']:
                # Send email notification
                send_mail(
                    f'Order #{self.id} Update - Frecha Iotech',
                    f"""
                    Dear {self.customer_name},
                    
                    {message}
                    
                    Order Details:
                    - Order ID: #{self.id}
                    - Service: {self.get_service_type_display()}
                    - Product: {self.product_details}
                    - Status: {self.get_status_display()}
                    - Total: TZS {self.total_price}
                    
                    Thank you for choosing Frecha Iotech!
                    
                    Best regards,
                    Frecha Iotech Team
                    """,
                    settings.DEFAULT_FROM_EMAIL,
                    [self.customer_email],
                    fail_silently=False,
                )
            
            if method in ['sms', 'both']:
                # SMS placeholder - you can integrate with Twilio, Africa's Talking, etc.
                sms_message = f"Frecha Iotech: {message}. Order #{self.id}"
                print(f"📱 SMS would be sent to {self.customer_phone}: {sms_message}")
                # Implement actual SMS sending based on your provider
            
            self.customer_notified = True
            self.notification_sent_at = timezone.now()
            self.notification_method = method
            self.save()
            
            return True
            
        except Exception as e:
            print(f"❌ Notification failed: {e}")
            return False