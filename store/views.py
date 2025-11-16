# store/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from .models import Order, ServiceProvider, DataBundle, RouterProduct, OrderTracking  # ← ADD OrderTracking
from .serializers import (
    OrderSerializer, OrderCreateSerializer, OrderUpdateSerializer, 
    ServiceProviderSerializer, DataBundleSerializer, RouterProductSerializer
)
# store/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')  # Replace with your home page name
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'store/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('home')  # Replace with your home page name
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'store/login.html')

@login_required
def profile(request):
    return render(request, 'store/profile.html', {'user': request.user})

# ============ ORDER VIEWSETS ============

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]  # Changed to AllowAny for public order creation
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                return Order.objects.all()
            else:
                return Order.objects.filter(user=user)
        else:
            return Order.objects.none()  # Public users can't view orders
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action in ['update', 'partial_update']:
            if self.request.user.is_staff:
                return OrderUpdateSerializer
            return OrderSerializer
        return OrderSerializer
    
    def perform_create(self, serializer):
        # Only set user if authenticated, otherwise create public order
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()  # Public order without user
    
    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=401)
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def status_counts(self, request):
        if request.user.is_staff:
            counts = {
                'total': Order.objects.count(),
                'pending': Order.objects.filter(status='pending').count(),
                'confirmed': Order.objects.filter(status='confirmed').count(),
                'processing': Order.objects.filter(status='processing').count(),
                'shipped': Order.objects.filter(status='shipped').count(),
                'delivered': Order.objects.filter(status='delivered').count(),
            }
        else:
            counts = {
                'total': Order.objects.filter(user=request.user).count(),
                'pending': Order.objects.filter(user=request.user, status='pending').count(),
                'confirmed': Order.objects.filter(user=request.user, status='confirmed').count(),
                'processing': Order.objects.filter(user=request.user, status='processing').count(),
                'shipped': Order.objects.filter(user=request.user, status='shipped').count(),
                'delivered': Order.objects.filter(user=request.user, status='delivered').count(),
            }
        return Response(counts)

class AdminOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return OrderUpdateSerializer
        return OrderSerializer
    
    @action(detail=True, methods=['post'])
    def mark_processing(self, request, pk=None):
        order = self.get_object()
        order.status = 'processing'
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_shipped(self, request, pk=None):
        order = self.get_object()
        order.status = 'shipped'
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_delivered(self, request, pk=None):
        order = self.get_object()
        order.mark_completed()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

# ============ SERVICE PROVIDER VIEWSETS ============

class ServiceProviderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for service providers (public access)
    """
    permission_classes = [permissions.AllowAny]
    queryset = ServiceProvider.objects.filter(is_active=True)
    serializer_class = ServiceProviderSerializer
    
    @action(detail=True, methods=['get'])
    def bundles(self, request, pk=None):
        """Get bundles for a specific provider"""
        provider = self.get_object()
        bundles = DataBundle.objects.filter(provider=provider, is_active=True)
        serializer = DataBundleSerializer(bundles, many=True)
        return Response({
            'provider': ServiceProviderSerializer(provider).data,
            'bundles': serializer.data
        })

class AdminServiceProviderViewSet(viewsets.ModelViewSet):
    """
    Admin ViewSet for managing service providers
    """
    permission_classes = [permissions.IsAdminUser]
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a service provider"""
        provider = self.get_object()
        provider.is_active = True
        provider.save()
        return Response({'status': 'provider activated'})
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a service provider"""
        provider = self.get_object()
        provider.is_active = False
        provider.save()
        return Response({'status': 'provider deactivated'})

# ============ DATA BUNDLE VIEWSETS ============

class DataBundleViewSet(viewsets.ModelViewSet):
    """
    Public ViewSet for data bundles
    """
    permission_classes = [permissions.AllowAny]
    queryset = DataBundle.objects.filter(is_active=True)
    serializer_class = DataBundleSerializer
    
    def get_queryset(self):
        queryset = DataBundle.objects.filter(is_active=True)
        provider_id = self.request.query_params.get('provider')
        if provider_id:
            queryset = queryset.filter(provider_id=provider_id)
        return queryset

class AdminDataBundleViewSet(viewsets.ModelViewSet):
    """
    Admin ViewSet for managing data bundles
    """
    permission_classes = [permissions.IsAdminUser]
    queryset = DataBundle.objects.all()
    serializer_class = DataBundleSerializer
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a data bundle"""
        bundle = self.get_object()
        bundle.is_active = True
        bundle.save()
        return Response({'status': 'bundle activated'})
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a data bundle"""
        bundle = self.get_object()
        bundle.is_active = False
        bundle.save()
        return Response({'status': 'bundle deactivated'})

# ============ ROUTER PRODUCT VIEWSETS ============

class RouterProductViewSet(viewsets.ModelViewSet):
    """
    Public ViewSet for router products
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = RouterProductSerializer
    
    def get_queryset(self):
        try:
            return RouterProduct.objects.filter(is_available=True)
        except Exception as e:
            print(f"Error in RouterProductViewSet: {e}")
            return RouterProduct.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {'error': 'Failed to fetch routers', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AdminRouterProductViewSet(viewsets.ModelViewSet):
    """
    Admin ViewSet for managing router products
    """
    permission_classes = [permissions.IsAdminUser]
    queryset = RouterProduct.objects.all()
    serializer_class = RouterProductSerializer
    
    @action(detail=True, methods=['post'])
    def make_available(self, request, pk=None):
        """Make a router product available"""
        router = self.get_object()
        router.is_available = True
        router.save()
        return Response({'status': 'router made available'})
    
    @action(detail=True, methods=['post'])
    def make_unavailable(self, request, pk=None):
        """Make a router product unavailable"""
        router = self.get_object()
        router.is_available = False
        router.save()
        return Response({'status': 'router made unavailable'})

# ============ FUNCTION-BASED VIEWS ============

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_status(request):
    """API status endpoint"""
    return Response({
        'status': 'API is running', 
        'timestamp': timezone.now(),
        'services_available': True
    })

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_providers(request):
    """Public endpoint to get all active service providers"""
    try:
        providers = ServiceProvider.objects.filter(is_active=True)
        serializer = ServiceProviderSerializer(providers, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch providers', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_bundles(request):
    """Public endpoint to get all active data bundles"""
    try:
        bundles = DataBundle.objects.filter(is_active=True).select_related('provider')
        serializer = DataBundleSerializer(bundles, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch bundles', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_routers(request):
    """Public endpoint to get all available router products"""
    try:
        routers = RouterProduct.objects.filter(is_available=True)
        serializer = RouterProductSerializer(routers, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch routers', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def all_services(request):
    """Get all services in one endpoint"""
    try:
        providers = ServiceProvider.objects.filter(is_active=True)
        bundles = DataBundle.objects.filter(is_active=True).select_related('provider')
        routers = RouterProduct.objects.filter(is_available=True)
        
        return Response({
            'providers': ServiceProviderSerializer(providers, many=True).data,
            'bundles': DataBundleSerializer(bundles, many=True).data,
            'routers': RouterProductSerializer(routers, many=True).data
        })
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch services', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def provider_bundles(request, provider_id):
    """Get bundles for a specific provider"""
    try:
        provider = ServiceProvider.objects.get(id=provider_id, is_active=True)
        bundles = DataBundle.objects.filter(provider=provider, is_active=True)
        
        return Response({
            'provider': ServiceProviderSerializer(provider).data,
            'bundles': DataBundleSerializer(bundles, many=True).data
        })
    except ServiceProvider.DoesNotExist:
        return Response({'error': 'Provider not found'}, status=404)
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch provider bundles', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_order(request):
    """Create a new order (public access)"""
    try:
        # Prepare order data from frontend
        order_data = {
            'customer_name': request.data.get('customer_name', ''),
            'customer_email': request.data.get('customer_email', ''),
            'customer_phone': request.data.get('customer_phone', ''),
            'product_details': request.data.get('product_details', ''),
            'quantity': request.data.get('quantity', 1),
            'total_price': request.data.get('total_price', 0.00),
            'notes': request.data.get('additional_notes', ''),
        }
        
        serializer = OrderCreateSerializer(data=order_data)
        if serializer.is_valid():
            # For public orders, don't associate with user
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response(
            {'error': 'Failed to create order', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_login(request):
    """User login endpoint"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff
            }
        })
    else:
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def user_logout(request):
    """User logout endpoint"""
    logout(request)
    return Response({'message': 'Logged out successfully'})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    """Get current user info"""
    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'is_staff': request.user.is_staff,
        'is_authenticated': True
    })

# ============ ADMIN ORDER MANAGEMENT ============

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def admin_order_stats(request):
    """Get order statistics for admin dashboard"""
    try:
        from django.db.models import Count
        
        stats = {
            'total_orders': Order.objects.count(),
            'pending_orders': Order.objects.filter(status='pending').count(),
            'completed_orders': Order.objects.filter(status='delivered').count(),
            'recent_orders': Order.objects.filter(created_at__gte=timezone.now() - timezone.timedelta(days=7)).count(),
            'status_breakdown': {
                status_val: Order.objects.filter(status=status_val).count()
                for status_val, _ in Order.STATUS_CHOICES
            }
        }
        
        return Response(stats)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def admin_update_order_status(request, order_id):
    """Update order status and send notification"""
    try:
        order = Order.objects.get(id=order_id)
        new_status = request.data.get('status')
        admin_notes = request.data.get('admin_notes', '')
        send_notification = request.data.get('send_notification', True)
        notification_method = request.data.get('notification_method', 'email')
        
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=400)
        
        # Update order
        order.status = new_status
        if admin_notes:
            order.admin_notes = admin_notes
        
        if new_status == 'delivered':
            order.completed_at = timezone.now()
        
        order.save()
        
        # Send notification if requested
        notification_sent = False
        if send_notification:
            message = request.data.get('custom_message') or f"Your order status has been updated to: {order.get_status_display()}"
            notification_sent = order.send_notification(method=notification_method, message=message)
        
        return Response({
            'message': 'Order updated successfully',
            'order': OrderSerializer(order).data,
            'notification_sent': notification_sent
        })
        
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def admin_send_notification(request, order_id):
    """Send custom notification to customer"""
    try:
        order = Order.objects.get(id=order_id)
        message = request.data.get('message')
        method = request.data.get('method', 'email')
        
        if not message:
            return Response({'error': 'Message is required'}, status=400)
        
        success = order.send_notification(method=method, message=message)
        
        return Response({
            'success': success,
            'message': 'Notification sent successfully' if success else 'Notification failed'
        })
        
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])  # Public for testing
def admin_search_orders(request):
    """Search orders by customer name, email, phone, or product"""
    try:
        query = request.GET.get('q', '')
        
        if not query:
            orders = Order.objects.all().order_by('-created_at')[:50]  # Limit for performance
        else:
            orders = Order.objects.filter(
                Q(customer_name__icontains=query) |
                Q(customer_email__icontains=query) |
                Q(customer_phone__icontains=query) |
                Q(product_details__icontains=query)
            ).order_by('-created_at')
        
        return Response({
            'results': OrderSerializer(orders, many=True).data,
            'count': orders.count()
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)

# ============ ORDER TRACKING VIEWS ============

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def guest_order_signup(request):
    """Allow guests to sign up for order tracking without full registration"""
    try:
        order_id = request.data.get('order_id')
        customer_email = request.data.get('customer_email')
        customer_phone = request.data.get('customer_phone', '')
        
        # Find order by ID and verify customer email matches
        order = Order.objects.get(
            id=order_id,
            customer_email=customer_email
        )
        
        # Create or get tracking
        tracking, created = OrderTracking.objects.get_or_create(
            order=order,
            defaults={
                'customer_email': customer_email,
                'customer_phone': customer_phone
            }
        )
        
        if created:
            # Send welcome email with tracking info
            tracking.add_status_update('registered', 'Customer signed up for tracking')
            
        return Response({
            'success': True,
            'tracking_number': tracking.tracking_number,
            'order_status': order.status,
            'customer_name': order.customer_name,
            'message': 'Order tracking activated successfully'
        })
        
    except Order.DoesNotExist:
        return Response(
            {'error': 'Order not found. Please check your order ID and email.'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': 'Failed to activate tracking', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def track_order(request, tracking_number):
    """Public endpoint to track order status"""
    try:
        tracking = OrderTracking.objects.get(
            tracking_number=tracking_number,
            is_active=True
        )
        order = tracking.order
        
        return Response({
            'tracking_number': tracking.tracking_number,
            'order_status': order.status,
            'status_display': order.get_status_display(),
            'customer_name': order.customer_name,
            'product_details': order.product_details,
            'order_date': order.created_at,
            'status_updates': tracking.status_updates,
            'estimated_delivery': order.estimated_delivery,
            'customer_support_email': 'support@frechaiotech.com'
        })
        
    except OrderTracking.DoesNotExist:
        return Response(
            {'error': 'Tracking number not found'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def update_order_tracking(request, order_id):
    """Admin update order tracking status"""
    try:
        order = Order.objects.get(id=order_id)
        new_status = request.data.get('status')
        admin_notes = request.data.get('notes', '')
        
        # Update order status
        order.status = new_status
        order.save()
        
        # Add to tracking history
        if hasattr(order, 'tracking'):
            order.tracking.add_status_update(new_status, admin_notes)
        
        return Response({
            'message': 'Order status updated',
            'order_status': order.status,
            'tracking_updates': order.tracking.status_updates if hasattr(order, 'tracking') else []
        })
        
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)