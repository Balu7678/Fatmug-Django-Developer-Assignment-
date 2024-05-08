from rest_framework import status
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Vendor,PurchaseOrder
from .serializers import VendorSerializer,PurchaseOrderSerializer,VendorPerformanceSerializer

@api_view(['GET', 'POST'])
def vendor_list(request):
    if request.method == 'GET':
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def vendor_detail(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def purchase_order_list(request):
    if request.method == 'GET':
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def purchase_order_detail(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET','POST'])
def vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VendorPerformanceSerializer(vendor)
        return Response(serializer.data)
    elif request.method == 'POST':
        vendor.on_time_delivery_rate = request.data.get('on_time_delivery_rate', vendor.on_time_delivery_rate)
        vendor.quality_rating = request.data.get('quality_rating', vendor.quality_rating)
        vendor.response_time = request.data.get('response_time', vendor.response_time)
        vendor.fulfillment_rate = request.data.get('fulfillment_rate', vendor.fulfillment_rate)

    
        vendor.save()
        return Response({'message': 'Vendor performance updated successfully'}, status=status.HTTP_201_CREATED)
    



