# store/serializers.py - UPDATED with Product
from rest_framework import serializers
from .models import ServiceProvider, DataBundle, RouterProduct, Order, Product  # ✅ Now Product exists

class ProductSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'product_type', 'price', 'description', 
            'is_active', 'provider', 'provider_name', 'data_amount', 
            'validity', 'color', 'image', 'specifications', 'created_at'
        ]

class ServiceProviderSerializer(serializers.ModelSerializer):
    bundle_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceProvider
        fields = ['id', 'name', 'is_active', 'bundle_count']
    
    def get_bundle_count(self, obj):
        return obj.bundles.count()

class DataBundleSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.name', read_only=True)
    
    class Meta:
        model = DataBundle
        fields = ['id', 'name', 'provider', 'provider_name', 'price', 'data_amount']
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be positive")
        return value

class RouterProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouterProduct
        fields = ['id', 'name', 'price']
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be positive")
        return value

class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', read_only=True, max_digits=10, decimal_places=2)
    
    class Meta:
        model = Order
        fields = [
            'id', 
            'customer_name', 
            'email',
            'phone', 
            'service_type', 
            'product',  # ✅ Now it's a ForeignKey
            'product_name',  # ✅ Read-only field
            'product_price', # ✅ Read-only field
            'package_details',
            'additional_notes',
            'status', 
            'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'product_name', 'product_price']