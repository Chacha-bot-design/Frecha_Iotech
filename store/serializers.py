from rest_framework import serializers
from .models import ServiceProvider, DataBundle, RouterProduct, Order


# ----------------------------
# Service Provider Serializer
# ----------------------------
class ServiceProviderSerializer(serializers.ModelSerializer):
    bundle_count = serializers.SerializerMethodField()

    class Meta:
        model = ServiceProvider
        fields = ['id', 'name', 'is_active', 'bundle_count']

    def get_bundle_count(self, obj):
        return obj.bundles.count()


# ----------------------------
# Data Bundle Serializer
# ----------------------------
class DataBundleSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.name', read_only=True)

    class Meta:
        model = DataBundle
        fields = ['id', 'name', 'provider', 'provider_name', 'price', 'data_amount', 'validity', 'description']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be positive")
        return value


# ----------------------------
# Router Product Serializer
# ----------------------------
class RouterProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouterProduct
        fields = ['id', 'name', 'price', 'color', 'image', 'specifications']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be positive")
        return value


# ----------------------------
# Order Serializer (Updated)
# ----------------------------
class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField(read_only=True)  # <-- display product name in responses

    class Meta:
        model = Order
        fields = [
            'id',
            'customer_name',
            'email',
            'phone',
            'service_type',
            'product_id',
            'product_name',
            'package_details',
            'additional_notes',
            'status',
            'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'product_name']

    # ✅ Validate that product_id belongs to the correct type (bundle or router)
    def validate(self, data):
        service_type = data.get('service_type')
        product_id = data.get('product_id')

        if not product_id:
            raise serializers.ValidationError({"product_id": "This field is required."})

        if service_type == 'bundle':
            if not DataBundle.objects.filter(id=product_id).exists():
                raise serializers.ValidationError({"product_id": "Invalid Data Bundle ID."})
        elif service_type == 'router':
            if not RouterProduct.objects.filter(id=product_id).exists():
                raise serializers.ValidationError({"product_id": "Invalid Router Product ID."})
        else:
            raise serializers.ValidationError({"service_type": "Invalid service type. Must be 'bundle' or 'router'."})

        return data

    # ✅ Add a readable product name in API responses
    def get_product_name(self, obj):
        if obj.service_type == 'bundle':
            product = DataBundle.objects.filter(id=obj.product_id).first()
        else:
            product = RouterProduct.objects.filter(id=obj.product_id).first()
        return product.name if product else None
