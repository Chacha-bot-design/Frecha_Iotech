from django.db import models

class ServiceProvider(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class DataBundle(models.Model):
    name = models.CharField(max_length=100)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    data_amount = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class RouterProduct(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"