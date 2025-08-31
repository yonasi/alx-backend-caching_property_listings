from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .utils import get_all_properties

@cache_page(60 * 15)  # Cache the view response for 15 minutes
def property_list(request):
    properties = get_all_properties()  # Use the cached queryset
    property_list = [
        {
            'id': prop.id,
            'title': prop.title,
            'description': prop.description,
            'price': str(prop.price),  # Convert Decimal to string for JSON
            'location': prop.location,
            'created_at': prop.created_at.isoformat()  # Convert DateTime to string
        } for prop in properties
    ]
    return JsonResponse({'data': property_list}, safe=False)