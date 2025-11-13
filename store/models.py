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

class Order(models.Model):
    customer_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service_type = models.CharField(max_length=50, choices=[('bundle','Data Bundle'), ('router','Router')])
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')
    package_details = models.TextField(blank=True)
    additional_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ])
