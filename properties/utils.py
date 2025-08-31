from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Check if the queryset is in Redis
    properties = cache.get('all_properties')
    
    if properties is None:
        # If not in cache, fetch from database
        properties = Property.objects.all()
        # Store in Redis with 1-hour TTL (3600 seconds)
        cache.set('all_properties', properties, 3600)
    
    return properties