import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.core.mail import send_mail  # <--- Import this
from django.template.loader import render_to_string # <--- Import this
from orders.models import Order
from cart.cart import Cart
from .models import Payment

# Initialize Razorpay
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def payment_process(request, order_id):
    # Fetch the PENDING order
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # If already paid, don't pay again
    if order.payment_status == 'PAID':
        return redirect('orders:order_detail', order_id=order.id)

    # Amount in Paise
    amount_in_paise = int(order.total_amount * 100)

    try:
        # Create Order on Razorpay
        razorpay_order_data = {
            'amount': amount_in_paise,
            'currency': 'INR',
            'payment_capture': '1',
            'notes': {
                'order_id': order.id,
                'site': 'CaseHaven'
            }
        }

        razorpay_order = client.order.create(data=razorpay_order_data)

        # Store Payment Record (Created)
        Payment.objects.update_or_create(
            order=order,
            defaults={
                'razorpay_order_id': razorpay_order['id'],
                'amount': order.total_amount,
                'status': 'CREATED',
                'gateway': 'RAZORPAY'
            }
        )

        context = {
            'order': order,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount_in_paise': amount_in_paise,
            'user_email': request.user.email,
            'user_contact': getattr(order, 'phone', ''),
        }
        return render(request, 'payments/process.html', context)

    except Exception as e:
        messages.error(request, f"Gateway Error: {str(e)}")
        return redirect('orders:checkout')


@csrf_exempt
def payment_verify(request):
    if request.method == 'POST':
        data = request.POST
        try:
            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_signature = data.get('razorpay_signature')

            # 1. Verify Signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            client.utility.verify_payment_signature(params_dict)

            # 2. Update Payment & Order
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.status = 'SUCCESS'
            payment.save()

            order = payment.order
            order.payment_status = 'PAID'
            # IMPORTANT: We do NOT set 'CONFIRMED' yet.
            # It stays 'ORDER_PLACED' until the Owner verifies stock/address.
            order.order_status = 'ORDER_PLACED'
            order.save()

            # 3. Clear Cart
            cart = Cart(request)
            cart.clear()

            # ==========================================
            # 4. SEND NOTIFICATIONS (NEW CODE)
            # ==========================================

            # A. Email to Shop Owner (Admin)
            subject_admin = f"🔔 New Order #{order.id} Received!"
            message_admin = (
                f"New Order Received!\n\n"
                f"Order ID: #{order.id}\n"
                f"Customer: {order.full_name}\n"
                f"Amount: ₹{order.total_amount}\n"
                f"Status: PAID\n\n"
                f"Please log in to the admin panel to process this order."
            )

            # We use fail_silently=True so payment flow doesn't crash if email fails
            send_mail(
                subject_admin,
                message_admin,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=True
            )

            # B. Email to Customer
            subject_user = f"Order Confirmed: #{order.id}"
            message_user = (
                f"Hi {order.full_name},\n\n"
                f"Thank you for your order! We have received your payment of ₹{order.total_amount}.\n"
                f"We will notify you once your items are shipped.\n\n"
                f"Order ID: #{order.id}\n\n"
                f"Thanks,\nCaseHaven Team"
            )

            send_mail(
                subject_user,
                message_user,
                settings.DEFAULT_FROM_EMAIL,
                [order.email],
                fail_silently=True
            )
            # ==========================================

            return render(request, 'payments/success.html', {'order': order})

        except razorpay.errors.SignatureVerificationError:
            return render(request, 'payments/failure.html', {'error': 'Signature Verification Failed'})
        except Exception as e:
            return render(request, 'payments/failure.html', {'error': str(e)})

    return HttpResponseBadRequest()