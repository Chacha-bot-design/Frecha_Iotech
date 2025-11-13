from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Order

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'title', 'description', 'created_at', 
                 'updated_at', 'status', 'status_display', 'admin_notes', 
                 'completed_at', 'tracking_number']
        read_only_fields = ['user', 'created_at', 'updated_at', 'completed_at']

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['title', 'description']

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status', 'admin_notes', 'tracking_number']