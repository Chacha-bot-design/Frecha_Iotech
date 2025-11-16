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

# ============ SEPARATED DATA MODELS ============

class DataPlan(models.Model):
    """Model for individual data plans"""
    DATA_TYPES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('special', 'Special Offer'),
        ('night', 'Night Bundle'),
        ('social', 'Social Media'),
        ('youtube', 'YouTube'),
        ('streaming', 'Streaming'),
    ]
    
    NETWORK_TYPES = [
        ('4g', '4G LTE'),
        ('5g', '5G'),
        ('3g', '3G'),
        ('2g', '2G'),
    ]
    
    name = models.CharField(max_length=255)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='data_plans')
    data_volume = models.CharField(max_length=50, help_text="e.g., 1GB, 500MB, Unlimited")
    validity_days = models.IntegerField(default=1, help_text="Validity in days")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    data_type = models.CharField(max_length=20, choices=DATA_TYPES, default='monthly')
    network_type = models.CharField(max_length=10, choices=NETWORK_TYPES, default='4g')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.provider.name} ({self.data_volume})"
    
    class Meta:
        verbose_name = "Data Plan"
        verbose_name_plural = "Data Plans"
        ordering = ['provider', 'price']

class Bundle(models.Model):
    """Model for bundled packages that can include multiple data plans"""
    BUNDLE_TYPES = [
        ('individual', 'Individual Bundle'),
        ('family', 'Family Bundle'),
        ('business', 'Business Bundle'),
        ('student', 'Student Bundle'),
        ('premium', 'Premium Bundle'),
    ]
    
    name = models.CharField(max_length=255)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='bundles')
    bundle_type = models.CharField(max_length=20, choices=BUNDLE_TYPES, default='individual')
    data_plans = models.ManyToManyField(DataPlan, related_name='bundles', blank=True)
    total_data_volume = models.CharField(max_length=50, help_text="Total data volume in bundle")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Discount percentage")
    description = models.TextField(blank=True)
    features = models.JSONField(default=list, help_text="List of features included")
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.provider.name}"
    
    def get_actual_price(self):
        """Calculate price after discount"""
        if self.discount_percentage > 0:
            discount_amount = (self.total_price * self.discount_percentage) / 100
            return self.total_price - discount_amount
        return self.total_price
    
    class Meta:
        verbose_name = "Bundle"
        verbose_name_plural = "Bundles"
        ordering = ['-is_featured', 'total_price']

# ============ ELECTRONICS DEVICES ============

class ElectronicsDevices(models.Model):
    CATEGORY_CHOICES = [
        ('laptops', 'Laptops'),
        ('smartphones', 'Smartphones'),
        ('tablets', 'Tablets'),
        ('accessories', 'Accessories'),
        ('gaming', 'Gaming Consoles'),
        ('audio', 'Audio Equipment'),
        ('cameras', 'Cameras'),
        ('networking', 'Networking Devices'),
        ('storage', 'Storage Devices'),
        ('other', 'Other Electronics'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    specifications = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='electronics/', blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Electronics Device"
        verbose_name_plural = "Electronics Devices"
        ordering = ['-created_at']

# ============ ORDER MODELS ============

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
        ('data_plan', 'Data Plan'),
        ('bundle', 'Bundle Package'),
        ('router', 'Router Product'),
        ('electronics', 'Electronics Device'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='orders')
    
    # Customer information
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    
    # Order details
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES, default='data_plan')
    product_details = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # References to specific products (optional)
    data_plan = models.ForeignKey(DataPlan, on_delete=models.SET_NULL, null=True, blank=True)
    bundle = models.ForeignKey(Bundle, on_delete=models.SET_NULL, null=True, blank=True)
    router_product = models.ForeignKey(RouterProduct, on_delete=models.SET_NULL, null=True, blank=True)
    electronics_device = models.ForeignKey(ElectronicsDevices, on_delete=models.SET_NULL, null=True, blank=True)
    
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

class OrderTracking(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='tracking')
    tracking_number = models.CharField(max_length=100, unique=True)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)
    signup_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # Tracking events
    status_updates = models.JSONField(default=list)
    
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