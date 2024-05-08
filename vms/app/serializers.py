from rest_framework import serializers
from .models import Vendor,PurchaseOrder

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'contact_details', 'address', 'vendor_code']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['id', 'po_number', 'vendor',  'items', 'quantity', 'status']



class VendorPerformanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = ['on_time_delivery_rate', 'quality_rating', 'response_time', 'fulfillment_rate']


