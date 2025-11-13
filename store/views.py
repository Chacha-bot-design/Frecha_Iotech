from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    """Create a new order with detailed debugging"""
    print("\n🚨 ========== CREATE_ORDER START ==========")
    try:
        # Log request body and metadata
        raw_body = request.body.decode('utf-8') if request.body else "Empty body"
        print("📦 Raw body:", raw_body)
        print("📦 Parsed data:", request.data)
        print("📦 Content type:", request.content_type)

        # Field-by-field analysis
        print("🔍 Field details:")
        for field in ['customer_name', 'email', 'phone', 'service_type', 'product_id', 'package_details', 'additional_notes']:
            print(f"   {field}: {repr(request.data.get(field))}")

        # product_id debugging
        pid = request.data.get('product_id')
        print(f"🔎 product_id raw: {repr(pid)} (type: {type(pid)})")

        # Run serializer
        serializer = OrderSerializer(data=request.data)
        print("🧪 Serializer created — validating...")

        if not serializer.is_valid():
            print("❌ Validation failed:", serializer.errors)
            return Response({
                "success": False,
                "error": "Validation failed",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        print("✅ Validation successful:", serializer.validated_data)

        # Save order
        order = serializer.save()
        print(f"🎉 Order saved! ID={order.id}, product_id={order.product_id}")

        # Return success response
        return Response({
            "success": True,
            "message": "Order created successfully",
            "order": OrderSerializer(order).data
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        import traceback
        print("💥 CRITICAL ERROR:", e)
        print(traceback.format_exc())
        return Response({
            "success": False,
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    finally:
        print("🚨 ========== CREATE_ORDER END ==========\n")
