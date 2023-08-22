from rest_framework.decorators import api_view
from .services import VendorService
from django.http import JsonResponse

vendor_service = VendorService()

@api_view(['GET'])
def weekly_vendors(request):
    vendors_data = vendor_service.get_weekly_vendors_data()
    return JsonResponse({'message':'Successfull','data':{'orders': vendors_data}})
