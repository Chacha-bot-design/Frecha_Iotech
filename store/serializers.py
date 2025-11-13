from rest_framework import serializers
from .models import ServiceProvider, DataBundle, RouterProduct, Order

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
    # Explicitly define to ensure it's included
    product_id = serializers.IntegerField()
    
    class Meta:
        model = Order
        fields = [
            'id', 
            'customer_name', 
            'email',           # ✅ ADDED
            'phone',           # ✅ ADDED
            'service_type', 
            'product_id',      # ✅ ADDED
            'package_details', # ✅ ADDED
            'additional_notes', # ✅ ADDED
            'status', 
            'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at']
    
    def validate_product_id(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("Valid product ID is required")
        return value