# store/views.py - UPDATE create_order function with more debugging
@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    """Create a new order"""
    print("🚨 ========== CREATE_ORDER START ==========")
    
    try:
        # Log the raw request body to see exactly what's received
        print("📦 Raw request body:", request.body.decode('utf-8') if request.body else "Empty body")
        print("📦 Parsed request data:", request.data)
        print("📦 Request content type:", request.content_type)
        
        # Detailed field analysis
        print("🔍 Detailed field analysis:")
        fields_to_check = ['customer_name', 'email', 'phone', 'service_type', 'product_id', 'package_details', 'additional_notes']
        for field in fields_to_check:
            value = request.data.get(field)
            print(f"   {field}: {repr(value)} (type: {type(value)})")
        
        # Check if product_id is specifically problematic
        product_id_raw = request.data.get('product_id')
        print(f"🔍 product_id analysis:")
        print(f"   Raw value: {repr(product_id_raw)}")
        print(f"   Type: {type(product_id_raw)}")
        print(f"   Is None: {product_id_raw is None}")
        print(f"   Is empty string: {product_id_raw == ''}")
        
        # Test the serializer step by step
        print("🧪 Creating serializer...")
        from .serializers import OrderSerializer
        serializer = OrderSerializer(data=request.data)
        print("✅ Serializer created")
        
        print("🧪 Running serializer validation...")
        is_valid = serializer.is_valid()
        print(f"✅ Validation result: {is_valid}")
        
        if not is_valid:
            print("❌ Serializer validation failed")
            print("🔍 Validation errors:", serializer.errors)
            return Response({
                "success": False,
                "error": "Data validation failed",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        print("✅ Serializer is valid")
        print("🔍 Validated data:", serializer.validated_data)
        print("🔍 Validated product_id:", serializer.validated_data.get('product_id'))
        print("🔍 Validated product_id type:", type(serializer.validated_data.get('product_id')))
        
        # Try to save
        print("🧪 Saving order...")
        order = serializer.save()
        print(f"🎉 Order saved successfully! ID: {order.id}")
        print(f"🎉 Saved product_id: {order.product_id}")
        
        return Response({
            "success": True,
            "message": "Order created successfully!",
            "order_id": order.id,
            "status": order.status
        }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        print(f"💥 CRITICAL ERROR: {str(e)}")
        import traceback
        error_traceback = traceback.format_exc()
        print(f"🔍 FULL TRACEBACK:\n{error_traceback}")
        
        return Response({
            "success": False,
            "error": f"Internal server error: {str(e)}",
            "traceback": error_traceback
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    finally:
        print("🚨 ========== CREATE_ORDER END ==========")