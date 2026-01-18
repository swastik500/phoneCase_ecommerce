from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import AddressForm
from .models import Address
from orders.models import Order


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after signup
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    addresses = request.user.addresses.all()
    return render(request, 'accounts/profile.html', {
        'orders': orders,
        'addresses': addresses
    })


@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            # Save address but attach the current user first
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('accounts:profile')
    else:
        form = AddressForm()

    return render(request, 'accounts/add_address.html', {'form': form})