from rest_framework import serializers
from .models import Order, Product

class OrderSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        required=True,
        source='product'  # Assuming your Order model has a ForeignKey `product`
    )

    class Meta:
        model = Order
        fields = [
            'customer_name',
            'email',
            'phone',
            'service_type',
            'product_id',
            'package_details',
            'additional_notes',
        ]

    def validate(self, data):
        # Ensure that product_id is provided for bundles or routers
        if not data.get('product'):
            raise serializers.ValidationError({'product_id': 'This field is required.'})
        return data
