from django.core.cache import cache
from .models import Property
import logging
from django.core.cache import cache
from django_redis import get_redis_connection
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



# Set up logging
logger = logging.getLogger(__name__)

def get_all_properties():
    properties = cache.get('all_properties')
    if properties is None:
        properties = Property.objects.all()
        cache.set('all_properties', properties, 3600)
    return properties

def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    Returns a dictionary with hits, misses, and hit ratio.
    """
    try:
        # Connect to Redis using django_redis
        redis_conn = get_redis_connection('default')
        
        # Get INFO stats from Redis
        info = redis_conn.info('stats')
        
        # Retrieve keyspace_hits and keyspace_misses
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        
        # Calculate hit ratio
        total = hits + misses
        hit_ratio = hits / total if total > 0 else 0.0
        
        # Log metrics
        logger.info(
            f"Redis Cache Metrics: hits={hits}, misses={misses}, hit_ratio={hit_ratio:.2%}"
        )
        
        # Return metrics dictionary
        return {
            'hits': hits,
            'misses': misses,
            'hit_ratio': hit_ratio
        }
    except Exception as e:
        # Log any errors
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}")
        return {
            'hits': 0,
            'misses': 0,
            'hit_ratio': 0.0
        }