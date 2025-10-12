# store/views.py - SIMPLER RESPONSES
@api_view(['GET'])
@permission_classes([AllowAny])
def public_providers(request):
    """Public providers list - returns array directly"""
    data = [
        {"id": 1, "name": "Provider 1", "type": "Basic"},
        {"id": 2, "name": "Provider 2", "type": "Basic"}
    ]
    return Response(data)  # Return array directly, not object

@api_view(['GET']) 
@permission_classes([AllowAny])
def public_bundles(request):
    """Public bundles list - returns array directly"""
    data = [
        {"id": 1, "name": "Starter Bundle", "price": "99.99"},
        {"id": 2, "name": "Business Bundle", "price": "199.99"}
    ]
    return Response(data)  # Return array directly, not object

@api_view(['GET'])
@permission_classes([AllowAny])
def public_routers(request):
    """Public routers list - returns array directly"""
    data = [
        {"id": 1, "name": "Home Router", "type": "Basic"},
        {"id": 2, "name": "Office Router", "type": "Professional"}
    ]
    return Response(data)  # Return array directly, not object