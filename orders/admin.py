from django.contrib import admin
from django.utils import timezone
from .models import Order, OrderItem, OrderUpdate


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


class OrderUpdateInline(admin.TabularInline):
    model = OrderUpdate
    extra = 0
    readonly_fields = ['timestamp']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'total_amount', 'payment_status', 'order_status', 'created_at']
    list_filter = ['payment_status', 'order_status', 'created_at']
    search_fields = ['full_name', 'email', 'id', 'tracking_id']
    inlines = [OrderItemInline, OrderUpdateInline]

    fieldsets = (
        ('Customer Info', {'fields': ('user', 'full_name', 'email', 'phone')}),
        ('Shipping Address', {'fields': ('address_line1', 'address_line2', 'city', 'state', 'pincode')}),
        ('Order Data', {'fields': ('total_amount', 'payment_status', 'order_status')}),
        ('Logistics', {'fields': ('courier_name', 'tracking_id', 'tracking_url', 'estimated_delivery_date')}),
    )

    actions = ['mark_packed', 'mark_shipped', 'mark_out_for_delivery', 'mark_delivered']

    def mark_packed(self, request, queryset):
        for order in queryset:
            order.order_status = 'PACKED'
            order.save()
            OrderUpdate.objects.create(order=order, status="Packed", description="Seller has packed your order.")

    mark_packed.short_description = "Step 1: Mark as Packed"

    def mark_shipped(self, request, queryset):
        for order in queryset:
            if not order.tracking_id:
                self.message_user(request, f"Error: Order {order.id} missing Tracking ID.", level='error')
                continue
            order.order_status = 'SHIPPED'
            order.save()
            OrderUpdate.objects.create(order=order, status="Shipped",
                                       description=f"Shipped via {order.courier_name or 'Courier'}. In Transit.")

    mark_shipped.short_description = "Step 2: Mark as Shipped (Req: Tracking ID)"

    def mark_out_for_delivery(self, request, queryset):
        for order in queryset:
            order.order_status = 'OUT_FOR_DELIVERY'
            order.save()
            OrderUpdate.objects.create(order=order, status="Out for Delivery", description="Agent is out for delivery.")

    mark_out_for_delivery.short_description = "Step 3: Mark Out for Delivery"

    def mark_delivered(self, request, queryset):
        for order in queryset:
            order.order_status = 'DELIVERED'
            order.save()
            OrderUpdate.objects.create(order=order, status="Delivered",
                                       description=f"Package delivered on {timezone.now().strftime('%d %b, %I:%M %p')}")

    mark_delivered.short_description = "Step 4: Mark as Delivered"