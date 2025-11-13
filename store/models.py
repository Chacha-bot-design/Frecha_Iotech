# store/models.py - WITH IMAGE FIELDS
from django.db import models

class ServiceProvider(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='providers/', blank=True, null=True)
    color = models.CharField(max_length=7, default='#000000')
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
    color = models.CharField(max_length=7, default='#000000')
    image = models.ImageField(upload_to='routers/', blank=True, null=True)
    specifications = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

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
    product_id = models.IntegerField()
    package_details = models.TextField(blank=True)
    additional_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending', choices=STATUS_CHOICES)
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"