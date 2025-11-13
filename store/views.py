# store/views.py - FIXED IMPORTS
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status  # ✅ Add this
from .serializers import OrderSerializer
from .models import Order, Product  # ✅ Add Product import if using new structure

# If you're keeping the old structure for now, use this:
@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    """Create a new order"""
    try:
        print("📦 Received data:", request.data)  # Add logging
        
        # For now, let's use the old structure since Product model doesn't exist yet
        data = request.data
        
        # Validate that product_id exists and is valid
        if 'product_id' not in data or not data['product_id']:
            return Response({
                "success": False,
                "error": "Product ID is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure product_id is a number
        try:
            data['product_id'] = int(data['product_id'])
        except (ValueError, TypeError):
            return Response({
                "success": False,
                "error": "Invalid product ID format"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            order = serializer.save()
            return Response({
                "success": True,
                "message": "Order created successfully!",
                "order_id": order.id,
                "status": order.status
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "success": False,
            "error": "Validation failed",
            "details": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        print(f"❌ Order creation error: {str(e)}")
        return Response({
            "success": False,
            "error": "Internal server error"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)