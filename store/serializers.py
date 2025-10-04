from rest_framework import serializers
from .models import Provider, Bundle, Router, Order

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'

class BundleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bundle
        fields = '__all__'

class RouterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Router
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'