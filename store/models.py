
from django.db import models


class ServiceProvider(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Service Provider"
        verbose_name_plural = "Service Providers"
class Order(models.Model):
    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    SERVICE_TYPES = (
        ('bundle', 'Data Bundle'),
        ('router', 'Router'),
    )
    
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    product_id = models.IntegerField()
    package_details = models.TextField(blank=True)
    additional_notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"
    
    def get_product_name(self):
        if self.service_type == 'bundle':
            try:
                from .models import DataBundle
                bundle = DataBundle.objects.get(id=self.product_id)
                return f"{bundle.provider.name} - {bundle.name}"
            except DataBundle.DoesNotExist:
                return "Unknown Bundle"
        else:
            try:
                from .models import RouterProduct
                router = RouterProduct.objects.get(id=self.product_id)
                return router.name
            except RouterProduct.DoesNotExist:
                return "Unknown Router"
    
    def get_total_price(self):
        if self.service_type == 'bundle':
            try:
                from .models import DataBundle
                bundle = DataBundle.objects.get(id=self.product_id)
                return bundle.price
            except DataBundle.DoesNotExist:
                return 0
        else:
            try:
                from .models import RouterProduct
                router = RouterProduct.objects.get(id=self.product_id)
                return router.price
            except RouterProduct.DoesNotExist:
                return 0
    
    class Meta:
        ordering = ['-created_at']  # Newest orders first

class ServiceProvider(models.Model):
    name = models.CharField(max_length=100)
    logo = models.CharField(max_length=100, help_text="Font Awesome icon class")
    color = models.CharField(max_length=7, default="#3498db")
    
    def __str__(self):
        return self.name

class DataBundle(models.Model):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    validity_days = models.IntegerField(default=30)
    
    def __str__(self):
        return f"{self.provider} - {self.name}"

class RouterProduct(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField(help_text="Comma-separated list of features")
    
    def __str__(self):
        return self.name

class Order(models.Model):
    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service_type = models.CharField(max_length=20, choices=(('bundle', 'Data Bundle'), ('router', 'Router')))
    product_id = models.IntegerField()
    package_details = models.TextField(blank=True)
    additional_notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"
    
    def get_product_name(self):
        if self.service_type == 'bundle':
            try:
                bundle = DataBundle.objects.get(id=self.product_id)
                return f"{bundle.provider.name} - {bundle.name}"
            except DataBundle.DoesNotExist:
                return "Unknown Bundle"
        else:
            try:
                router = RouterProduct.objects.get(id=self.product_id)
                return router.name
            except RouterProduct.DoesNotExist:
                return "Unknown Router"
    
    def get_total_price(self):
        if self.service_type == 'bundle':
            try:
                bundle = DataBundle.objects.get(id=self.product_id)
                return bundle.price
            except DataBundle.DoesNotExist:
                return 0
        else:
            try:
                router = RouterProduct.objects.get(id=self.product_id)
                return router.price
            except RouterProduct.DoesNotExist:
                return 0

# Create your models here.
