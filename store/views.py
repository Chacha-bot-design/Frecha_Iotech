from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login

# Public endpoint to check API status
@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    return Response({
        "status": "API is running",
        "authenticated": request.user.is_authenticated,
        "user": request.user.username if request.user.is_authenticated else None
    })

# Login endpoint for frontend
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        })
    else:
        return Response({"message": "Invalid credentials"}, status=401)

# Protected API endpoints
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bundle_list(request):
    return Response({
        "message": "Bundles data",
        "data": []  # Add your actual data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def provider_list(request):
    return Response({
        "message": "Providers data",
        "data": []  # Add your actual data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def router_list(request):
    return Response({
        "message": "Routers data", 
        "data": []  # Add your actual data
    })