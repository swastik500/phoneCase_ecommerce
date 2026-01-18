from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
import datetime

# Import models
from catalog.models import Product
from orders.models import Order, OrderUpdate
from payments.models import Payment


# --- HOMEPAGE VIEW ---
def home(request):
    featured_products = Product.objects.filter(is_active=True)[:4]
    return render(request, 'core/home.html', {'products': featured_products})


# --- OWNER DASHBOARD VIEW ---
@staff_member_required
def owner_dashboard(request):
    # 1. Key Metrics
    total_revenue = Order.objects.filter(payment_status='PAID').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_orders = Order.objects.count()
    # "Pending Shipments" means Confirmed but not yet Shipped
    pending_shipments = Order.objects.filter(order_status='CONFIRMED').count()
    low_stock_count = Product.objects.filter(stock__lt=5).count()

    # 2. Recent Data
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]

    # 3. Recent Payments
    recent_payments = Payment.objects.order_by('-created_at')[:5]

    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'pending_shipments': pending_shipments,
        'low_stock_count': low_stock_count,
        'recent_orders': recent_orders,
        'recent_payments': recent_payments,
    }
    return render(request, 'core/manager_dashboard.html', context)


# --- ORDER PROCESSING WORKSTATION ---
@staff_member_required
def process_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        # 1. CONFIRM ORDER
        if action == 'confirm':
            order.order_status = 'CONFIRMED'
            order.confirmed_at = timezone.now()
            # Calculate EDD (e.g., 5 days from now)
            order.estimated_delivery_date = timezone.now().date() + datetime.timedelta(days=5)
            order.save()
            OrderUpdate.objects.create(order=order, status="Order Confirmed",
                                       description="Seller has accepted your order.")
            messages.success(request, "Order Confirmed!")

        # 2. MARK AS PACKED
        elif action == 'pack':
            order.order_status = 'PACKED'
            order.packed_at = timezone.now()
            order.save()
            OrderUpdate.objects.create(order=order, status="Packed",
                                       description="Your item is packed and ready for dispatch.")
            messages.success(request, "Order Marked as Packed!")

        # 3. SHIP ORDER (Requires Courier Details)
        elif action == 'ship':
            courier = request.POST.get('courier_name')
            tracking = request.POST.get('tracking_id')
            if courier and tracking:
                order.order_status = 'SHIPPED'
                order.shipped_at = timezone.now()
                order.courier_name = courier
                order.tracking_id = tracking
                order.save()
                OrderUpdate.objects.create(order=order, status="Shipped",
                                           description=f"Shipped via {courier}. Tracking ID: {tracking}")
                messages.success(request, "Order Shipped Successfully!")
            else:
                messages.error(request, "Courier Name and Tracking ID are required.")

        # 4. MARK DELIVERED
        elif action == 'deliver':
            order.order_status = 'DELIVERED'
            order.delivered_at = timezone.now()
            order.save()
            OrderUpdate.objects.create(order=order, status="Delivered", description="Package delivered successfully.")
            messages.success(request, "Order Marked as Delivered!")

        return redirect('core:process_order', order_id=order.id)

    return render(request, 'core/process_order.html', {'order': order})