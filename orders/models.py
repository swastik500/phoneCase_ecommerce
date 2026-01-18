from django.db import models
from django.conf import settings
from catalog.models import Product
from django.utils import timezone
import datetime


class Order(models.Model):
    # Precise Status Flow
    ORDER_STATUS_CHOICES = (
        ('ORDER_PLACED', 'Order Placed'),  # Paid, waiting for admin
        ('CONFIRMED', 'Confirmed'),  # Admin accepted
        ('PACKED', 'Packed'),  # Box sealed
        ('SHIPPED', 'Shipped'),  # Handed to courier
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
        ('RETURNED', 'Returned'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')

    # Address Snapshot
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    # Money & Status
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='ORDER_PLACED')

    # Logistics Data
    courier_name = models.CharField(max_length=100, blank=True, null=True)
    tracking_id = models.CharField(max_length=100, blank=True, null=True)
    tracking_url = models.URLField(blank=True, null=True)
    estimated_delivery_date = models.DateField(blank=True, null=True)

    # TIMESTAMPS (The "When did it happen?" fields)
    created_at = models.DateTimeField(auto_now_add=True)  # Order Placed Time
    confirmed_at = models.DateTimeField(blank=True, null=True)  # Owner clicked Confirm
    packed_at = models.DateTimeField(blank=True, null=True)  # Owner clicked Packed
    shipped_at = models.DateTimeField(blank=True, null=True)  # Owner clicked Shipped
    delivered_at = models.DateTimeField(blank=True, null=True)  # Final delivery

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'Order #{self.id}'


# Timeline History (Keeps a log of text updates)
class OrderUpdate(models.Model):
    order = models.ForeignKey(Order, related_name='updates', on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity