# store/serializers.py
from rest_framework import serializers
from .models import (
    DataPlan, Bundle, ElectronicsDevices, Order, 
    ServiceProvider, RouterProduct, OrderTracking
)

class DataPlanSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.name', read_only=True)
    data_type_display = serializers.CharField(source='get_data_type_display', read_only=True)
    network_type_display = serializers.CharField(source='get_network_type_display', read_only=True)
    
    class Meta:
        model = DataPlan
        fields = [
            'id', 'name', 'provider', 'provider_name', 'data_volume', 'validity_days',
            'price', 'data_type', 'data_type_display', 'network_type', 'network_type_display',
            'description', 'is_active', 'created_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class BundleSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.name', read_only=True)
    bundle_type_display = serializers.CharField(source='get_bundle_type_display', read_only=True)
    actual_price = serializers.DecimalField(source='get_actual_price', read_only=True, max_digits=10, decimal_places=2)
    data_plans_details = DataPlanSerializer(source='data_plans', many=True, read_only=True)
    
    class Meta:
        model = Bundle
        fields = [
            'id', 'name', 'provider', 'provider_name', 'bundle_type', 'bundle_type_display',
            'data_plans', 'data_plans_details', 'total_data_volume', 'total_price',
            'actual_price', 'discount_percentage', 'description', 'features',
            'is_active', 'is_featured', 'created_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ElectronicsDevicesSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = ElectronicsDevices
        fields = [
            'id', 'name', 'description', 'price', 'category', 'category_display',
            'specifications', 'is_available', 'image', 'stock_quantity',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class OrderSerializer(serializers.ModelSerializer):
    service_type_display = serializers.CharField(source='get_service_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'customer_name', 'customer_email', 'customer_phone', 'service_type',
            'product_details', 'quantity', 'total_price', 'notes',
            'data_plan', 'bundle', 'router_product', 'electronics_device'
        ]

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status', 'admin_notes', 'tracking_number']

class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = '__all__'

class RouterProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouterProduct
        fields = '__all__'

class OrderTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTracking
        fields = '__all__'