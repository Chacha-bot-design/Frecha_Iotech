from rest_framework import serializers
from .models import ServiceProvider, DataBundle, RouterProduct, Order

class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = '__all__'

class DataBundleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataBundle
        fields = '__all__'

class RouterProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouterProduct
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'