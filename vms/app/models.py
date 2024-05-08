import datetime
from django.db import models
from django.utils import timezone


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating = models.FloatField(default=0)
    response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)
    def __str__(self):
        return self.name
    
    def update_performance_metrics(self):
        completed_orders = self.purchaseorder_set.filter(status='completed')

        on_time_delivery_count = completed_orders.filter(delivery_date__lte=models.F('issue_date')).count()
        total_completed_count = completed_orders.count()
        self.on_time_delivery_rate = (on_time_delivery_count / total_completed_count) * 100 if total_completed_count else 0

        
        quality_ratings = completed_orders.exclude(quality_rating__isnull=True).values_list('quality_rating', flat=True)
        self.quality_rating_avg = sum(quality_ratings) / len(quality_ratings) if quality_ratings else 0

        
        response_times = completed_orders.exclude(acknowledgment_date__isnull=True).annotate(
            response_time=models.F('acknowledgment_date') - models.F('issue_date')
        ).values_list('response_time', flat=True)
        self.average_response_time = sum(response_times, datetime.timedelta()) / len(response_times) if response_times else 0

    
        successful_orders = completed_orders.filter(issues__isnull=True)
        self.fulfillment_rate = (successful_orders.count() / total_completed_count) * 100 if total_completed_count else 0

        self.save()


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    order_date = models.DateField(default=timezone.now)
    items = models.TextField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')])

    def __str__(self):
        return self.po_number
    
    @property
    def is_completed(self):
        return self.status == 'completed'
