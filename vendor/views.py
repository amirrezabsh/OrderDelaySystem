from rest_framework.decorators import api_view
from .services import VendorService
from django.http import JsonResponse
from rest_framework.response import Response
vendor_service = VendorService()

# API call for getting vendors orderd by their delays for the past week
@api_view(['GET'])
def weekly_vendors(request):
    vendors_data = vendor_service.get_weekly_vendors_data()
    return Response(data={'message':'Successful','orders': vendors_data},status=200)
