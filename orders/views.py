from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from cart.cart import Cart
from .models import Order, OrderItem
from accounts.models import Address
from .models import Order, OrderItem, OrderUpdate # Import OrderUpdate
from django.http import Http404


@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        address_id = request.POST.get('address')
        # ... (address validation code same as before) ...
        try:
            address = Address.objects.get(id=address_id, user=request.user)
        except Address.DoesNotExist:
            return redirect('orders:checkout')

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                full_name=address.full_name,
                email=request.user.email,
                phone=address.phone,
                # ... (other address fields) ...
                address_line1=address.line1,
                address_line2=address.line2,
                city=address.city,
                state=address.state,
                pincode=address.pincode,
                total_amount=cart.get_total_price(),
                payment_status='PENDING',
                order_status='ORDER_PLACED'
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            # STAGE 1: Create Initial Tracking Entry
            OrderUpdate.objects.create(
                order=order,
                status="Order Placed",
                description="Order has been placed successfully. Waiting for payment."
            )

        return redirect('payments:process', order_id=order.id)

    addresses = request.user.addresses.all()
    return render(request, 'orders/checkout.html', {'cart': cart, 'addresses': addresses})


@login_required
def order_detail(request, order_id):
    # 1. Get the order regardless of who owns it
    order = get_object_or_404(Order, id=order_id)

    # 2. Check Permissions:
    # Allow if the logged-in user is the owner OR if they are Staff (Admin/Shop Owner)
    if order.user != request.user and not request.user.is_staff:
        raise Http404("Order not found")

    return render(request, 'orders/detail.html', {'order': order})