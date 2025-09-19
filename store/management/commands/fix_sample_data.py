from django.core.management.base import BaseCommand
from store.models import ServiceProvider, DataBundle, RouterProduct

class Command(BaseCommand):
    help = 'Creates safe sample data for the application'
    
    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # First, delete any existing data to avoid duplicates
        DataBundle.objects.all().delete()
        RouterProduct.objects.all().delete()
        ServiceProvider.objects.all().delete()
        
        # Create service providers
        providers_data = [
            {'name': 'Vodacom', 'logo': 'fas fa-sim-card', 'color': '#E60000'},
            {'name': 'Airtel', 'logo': 'fas fa-sim-card', 'color': '#FF0000'},
            {'name': 'Halotel', 'logo': 'fas fa-sim-card', 'color': '#00A0E0'},
            {'name': 'Yas', 'logo': 'fas fa-sim-card', 'color': '#FF9900'},
        ]
        
        providers = {}
        for data in providers_data:
            provider, created = ServiceProvider.objects.get_or_create(**data)
            providers[provider.name] = provider
            self.stdout.write(f'{"Created" if created else "Exists"}: {provider.name}')
        
        # Create data bundles
        bundles_data = [
            {'provider': providers['Vodacom'], 'name': '1GB Daily', 'description': '1GB data valid for 24 hours', 'price': 1000, 'validity_days': 1},
            {'provider': providers['Vodacom'], 'name': '5GB Weekly', 'description': '5GB data valid for 7 days', 'price': 5000, 'validity_days': 7},
            {'provider': providers['Vodacom'], 'name': '10GB Monthly', 'description': '10GB data valid for 30 days', 'price': 15000, 'validity_days': 30},
            {'provider': providers['Airtel'], 'name': '2GB Daily', 'description': '2GB data valid for 24 hours', 'price': 1500, 'validity_days': 1},
            {'provider': providers['Airtel'], 'name': '8GB Weekly', 'description': '8GB data valid for 7 days', 'price': 7000, 'validity_days': 7},
        ]
        
        for data in bundles_data:
            bundle, created = DataBundle.objects.get_or_create(**data)
            self.stdout.write(f'{"Created" if created else "Exists"}: {bundle.name}')
        
        # Create routers
        routers_data = [
            {'name': '4G LTE Router', 'description': 'High-speed wireless internet for home and office use', 'price': 120000, 'features': '4G LTE, WiFi 802.11n, Ethernet ports, SIM card slot'},
            {'name': 'Portable WiFi', 'description': 'Stay connected on the go with our portable WiFi devices', 'price': 85000, 'features': 'Portable, Battery powered, 4G LTE, WiFi hotspot'},
            {'name': 'Home Router', 'description': 'Reliable connectivity for your entire household', 'price': 65000, 'features': 'WiFi 802.11ac, Ethernet ports, Parental controls'},
        ]
        
        for data in routers_data:
            router, created = RouterProduct.objects.get_or_create(**data)
            self.stdout.write(f'{"Created" if created else "Exists"}: {router.name}')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))