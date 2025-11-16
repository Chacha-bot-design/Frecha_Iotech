# store/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

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
    
  class ElectronicsDevices(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    specifications = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='electronics/',blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    SERVICE_TYPES = [
        ('bundle', 'Data Bundle'),
        ('router', 'Router Product'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='orders')
    
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
    
    # Notification fields
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
                # SMS placeholder
                sms_message = f"Frecha Iotech: {message}. Order #{self.id}"
                print(f"📱 SMS would be sent to {self.customer_phone}: {sms_message}")
            
            self.customer_notified = True
            self.notification_sent_at = timezone.now()
            self.notification_method = method
            self.save()
            
            return True
            
        except Exception as e:
            print(f"❌ Notification failed: {e}")
            return False

# ✅ CORRECT: OrderTracking is a separate class, not inside Order
class OrderTracking(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='tracking')
    tracking_number = models.CharField(max_length=100, unique=True)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)
    signup_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # Tracking events
    status_updates = models.JSONField(default=list)  # Store status history
    
    def __str__(self):
        return f"Tracking #{self.tracking_number} - {self.order.customer_name}"

    def generate_tracking_number(self):
        return f"FRE{str(uuid.uuid4())[:8].upper()}"
    
    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = self.generate_tracking_number()
        super().save(*args, **kwargs)
    
    def add_status_update(self, status, notes=""):
        self.status_updates.append({
            'status': status,
            'notes': notes,
            'timestamp': timezone.now().isoformat()
        })
        self.save()