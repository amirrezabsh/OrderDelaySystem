from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    total_delays = serializers.IntegerField(read_only=True)

    class Meta:
        model = Vendor
        fields = ['id', 'name', 'total_delays']
