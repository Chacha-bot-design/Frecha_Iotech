# store/serializers.py - FIXED
from rest_framework import serializers
from .models import ServiceProvider, DataBundle, RouterProduct, Order

class ServiceProviderSerializer(serializers.ModelSerializer):
    bundle_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceProvider
        fields = ['id', 'name', 'description', 'logo', 'color', 'is_active', 'bundle_count']
    
    def get_bundle_count(self, obj):
        return obj.bundles.count()

class DataBundleSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.name', read_only=True)
    
    class Meta:
        model = DataBundle
        fields = ['id', 'name', 'description', 'price', 'provider', 'provider_name', 'data_amount', 'validity']
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be positive")
        return value

class RouterProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouterProduct
        fields = ['id', 'name', 'description', 'price', 'color', 'image', 'specifications']
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be positive")
        return value

class OrderSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    
    class Meta:
        model = Order
        fields = [
            'id', 
            'customer_name', 
            'email',
            'phone', 
            'service_type', 
            'product_id',
            'package_details',
            'additional_notes',
            'status', 
            'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at']
    
    def validate_product_id(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("Valid product ID is required")
        return value