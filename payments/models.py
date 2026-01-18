from django.db import models
from orders.models import Order


class Payment(models.Model):
    STATUS_CHOICES = (
        ('CREATED', 'Created'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    )

    order = models.OneToOneField(Order, related_name='payment', on_delete=models.CASCADE)
    gateway = models.CharField(max_length=20, default='RAZORPAY')

    # Razorpay specific fields
    razorpay_order_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CREATED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.razorpay_order_id} for Order {self.order.id}"