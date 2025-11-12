# store/views.py - REPLACE your create_order function with this:
@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    """Create a new order"""
    print("🚨 ========== CREATE_ORDER START ==========")
    
    try:
        # Log everything about the request
        print("📦 Request method:", request.method)
        print("📦 Content type:", request.content_type)
        print("📦 Headers:", dict(request.headers))
        print("📦 Full request data:", request.data)
        print("📦 User:", request.user)
        
        # Check if data is present
        if not request.data:
            print("❌ No data received")
            return Response({
                "success": False,
                "error": "No data provided"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Log each field individually with types
        print("🔍 Field-by-field analysis:")
        fields_to_check = ['customer_name', 'email', 'phone', 'service_type', 'product_id', 'package_details', 'additional_notes']
        for field in fields_to_check:
            value = request.data.get(field)
            print(f"   {field}: {value} (type: {type(value)})")
        
        # Check for missing required fields
        required_fields = ['customer_name', 'email', 'phone', 'service_type', 'product_id']
        missing_fields = [field for field in required_fields if not request.data.get(field)]
        
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
            return Response({
                "success": False,
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        print("✅ All required fields present")
        
        # Test database connection and model access
        print("🧪 Testing database connection...")
        try:
            order_count = Order.objects.count()
            print(f"✅ Database accessible. Total orders: {order_count}")
        except Exception as db_error:
            print(f"❌ Database error: {str(db_error)}")
            raise db_error
        
        # Test the serializer step by step
        print("🧪 Testing serializer creation...")
        serializer = OrderSerializer(data=request.data)
        print("✅ Serializer created")
        
        print("🧪 Testing serializer validation...")
        is_valid = serializer.is_valid()
        print(f"✅ Serializer validation result: {is_valid}")
        
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
        
        # Try to save the order
        print("🧪 Saving order to database...")
        try:
            order = serializer.save()
            print(f"🎉 Order saved successfully! ID: {order.id}")
            print(f"🎉 Order details: {order.customer_name}, {order.service_type}, product_id: {order.product_id}")
            
            return Response({
                "success": True,
                "message": "Order created successfully!",
                "order_id": order.id,
                "status": order.status
            }, status=status.HTTP_201_CREATED)
            
        except Exception as save_error:
            print(f"❌ Error saving order: {str(save_error)}")
            import traceback
            print(f"🔍 Save error traceback: {traceback.format_exc()}")
            raise save_error
            
    except Exception as e:
        print(f"💥 CRITICAL ERROR in create_order: {str(e)}")
        import traceback
        error_traceback = traceback.format_exc()
        print(f"🔍 FULL TRACEBACK:\n{error_traceback}")
        
        # Return the actual error for debugging
        return Response({
            "success": False,
            "error": f"Internal server error: {str(e)}",
            "traceback": error_traceback  # Include in response temporarily
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    finally:
        print("🚨 ========== CREATE_ORDER END ==========")