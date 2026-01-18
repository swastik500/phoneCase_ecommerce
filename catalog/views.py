from django.shortcuts import render, get_object_or_404
from django.db.models import Q  # Import Q for search lookups
from .models import Category, Product


def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)

    # Category Filter
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Search Logic
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description_short__icontains=query) |
            Q(category__name__icontains=query)
        )

    return render(request, 'catalog/list.html', {
        'products': products,
        'categories': categories,
        'search_query': query  # Pass query back to template to show "Results for..."
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'catalog/detail.html', {'product': product})