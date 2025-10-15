from rest_framework import serializers
from .models import ServiceProvider, DataBundle, RouterProduct, Order

class ServiceProviderSerializer(serializers.ModelSerializer):
    bundle_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceProvider
        fields = ['id', 'name', 'is_active', 'bundle_count']
    
    def get_bundle_count(self, obj):
        # Use the correct relationship name 'bundles' from your model
        return obj.bundles.count()  # ✅ FIXED: Changed from databundle to bundles

class DataBundleSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.name', read_only=True)
    
    class Meta:
        model = DataBundle
        fields = ['id', 'name', 'provider', 'provider_name', 'price', 'data_amount']
    
    def validate_price(self, value):
        """Ensure price is positive"""
        if value <= 0:
            raise serializers.ValidationError("Price must be positive")
        return value

class RouterProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouterProduct
        fields = ['id', 'name', 'price']
    
    def validate_price(self, value):
        """Ensure price is positive"""
        if value <= 0:
            raise serializers.ValidationError("Price must be positive")
        return value

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'service_type', 'status', 'created_at']
    
    def validate_service_type(self, value):
        """Validate service type"""
        valid_types = ['bundle', 'router', 'other']
        if value not in valid_types:
            raise serializers.ValidationError(f"Service type must be one of: {', '.join(valid_types)}")
        return value