from django.core.management.base import BaseCommand
from store.models import ServiceProvider, DataBundle, RouterProduct

class Command(BaseCommand):
    help = 'Load sample data for Frecha Iotech'
    
    def handle(self, *args, **options):
        # Create providers
        providers = [
            ServiceProvider(name="Vodacom", logo="fas fa-sim-card", color="#E60000"),
            ServiceProvider(name="Airtel", logo="fas fa-sim-card", color="#FF0000"),
            ServiceProvider(name="Halotel", logo="fas fa-sim-card", color="#00A0E0"),
            ServiceProvider(name="Yas", logo="fas fa-sim-card", color="#FF9900"),
        ]
        
        for provider in providers:
            provider.save()
        
        # Create bundles
        bundles = [
            DataBundle(provider=providers[0], name="1GB Daily", description="1GB for 24 hours", price=1000, validity_days=1),
            DataBundle(provider=providers[0], name="5GB Weekly", description="5GB for 7 days", price=5000, validity_days=7),
            DataBundle(provider=providers[0], name="10GB Monthly", description="10GB for 30 days", price=15000, validity_days=30),
            DataBundle(provider=providers[1], name="2GB Daily", description="2GB for 24 hours", price=1500, validity_days=1),
            DataBundle(provider=providers[1], name="8GB Weekly", description="8GB for 7 days", price=7000, validity_days=7),
        ]
        
        for bundle in bundles:
            bundle.save()
        
        # Create routers
        routers = [
            RouterProduct(name="4G LTE Router", description="High-speed wireless internet", price=120000, features="4G, WiFi, Ethernet"),
            RouterProduct(name="Portable WiFi", description="Stay connected on the go", price=85000, features="Portable, Battery"),
            RouterProduct(name="Home Router", description="Reliable connectivity", price=65000, features="WiFi, Ethernet"),
        ]
        
        for router in routers:
            router.save()
        
        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))