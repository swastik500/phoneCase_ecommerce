from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    # Updated list_display back to Razorpay fields
    list_display = ['id', 'order', 'razorpay_order_id', 'amount', 'status', 'created_at']
    list_filter = ['status']