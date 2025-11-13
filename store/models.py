from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class ServiceProvider(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='providers/', blank=True, null=True)
    color = models.CharField(max_length=7)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class DataBundle(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='bundles')
    data_amount = models.CharField(max_length=50, blank=True)
    validity = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.provider.name}"

class RouterProduct(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=7)
    image = models.ImageField(upload_to='routers/', blank=True, null=True)
    specifications = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    PRODUCT_TYPES = [
        ('bundle', 'Data Bundle'),
        ('router', 'Router'),
    ]
    
    name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # For bundles
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, null=True, blank=True, related_name='products')
    data_amount = models.CharField(max_length=50, blank=True)
    validity = models.CharField(max_length=50, blank=True)
    
    # For routers
    color = models.CharField(max_length=7, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    specifications = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_product_type_display()})"

class Order(models.Model):
    SERVICE_TYPES = [
        ('bundle', 'Data Bundle'),
        ('router', 'Router'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')  # ✅ Changed from product_id
    package_details = models.TextField(blank=True)
    additional_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending', choices=STATUS_CHOICES)
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"