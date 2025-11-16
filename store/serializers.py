# store/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Order, ServiceProvider, DataBundle, RouterProduct

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at']

class DataBundleSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.name', read_only=True)
    
    class Meta:
        model = DataBundle
        fields = [
            'id', 'name', 'provider', 'provider_name', 'price', 
            'data_volume', 'validity_days', 'description', 'is_active', 
            'created_at', 'updated_at'
        ]

class RouterProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouterProduct
        fields = [
            'id', 'name', 'description', 'price', 'specifications',
            'is_available', 'image', 'created_at', 'updated_at'
        ]

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    service_type_display = serializers.CharField(source='get_service_type_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'customer_name', 'customer_email', 'customer_phone',
            'service_type', 'service_type_display', 'product_details', 
            'quantity', 'total_price', 'status', 'status_display',
            'notes', 'admin_notes', 'tracking_number', 'created_at', 
            'updated_at', 'completed_at', 'customer_notified',
            'notification_sent_at', 'notification_method'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at', 'completed_at']

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'customer_name', 'customer_email', 'customer_phone',
            'service_type', 'product_details', 'quantity', 'total_price', 'notes'
        ]
        # ✅ ADD THIS TO MAKE FIELDS OPTIONAL
        extra_kwargs = {
            'service_type': {'required': False, 'default': 'bundle'},
            'quantity': {'required': False, 'default': 1},
            'total_price': {'required': False, 'default': 0.00},
            'notes': {'required': False, 'allow_blank': True}
        }

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status', 'admin_notes', 'tracking_number', 'completed_at']