from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, RFQ, Order
from .forms import ProductForm, RFQForm, OrderForm


def marketplace(request):
    market_type = request.GET.get('market', 'local')
    country = request.GET.get('country', '')
    category_slug = request.GET.get('category', '')
    query = request.GET.get('q', '')

    products = Product.objects.filter(is_active=True)

    if market_type == 'local':
        products = products.filter(market_type__in=['local', 'both'])
    else:
        products = products.filter(market_type__in=['international', 'both'])

    if country:
        products = products.filter(country=country)
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if query:
        products = products.filter(Q(title__icontains=query) | Q(description__icontains=query))

    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'market_type': market_type,
        'selected_country': country,
        'query': query,
        'country_choices': [
            ('CA', 'Canada'), ('UG', 'Uganda'), ('NL', 'Netherlands'),
            ('JP', 'Japan'), ('KE', 'Kenya'),
        ],
    }
    return render(request, 'ecommerce/marketplace.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    product.views_count += 1
    product.save(update_fields=['views_count'])
    related = Product.objects.filter(category=product.category, is_active=True).exclude(pk=product.pk)[:4]
    return render(request, 'ecommerce/product_detail.html', {'product': product, 'related': related})


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, 'Product listed successfully!')
            return redirect('marketplace')
    else:
        form = ProductForm()
    return render(request, 'ecommerce/add_product.html', {'form': form})


@login_required
def submit_rfq(request):
    if request.method == 'POST':
        form = RFQForm(request.POST)
        if form.is_valid():
            rfq = form.save(commit=False)
            rfq.buyer = request.user
            rfq.save()
            messages.success(request, 'RFQ submitted. Suppliers will respond shortly.')
            return redirect('my_rfqs')
    else:
        form = RFQForm()
    return render(request, 'ecommerce/rfq_form.html', {'form': form})


@login_required
def my_rfqs(request):
    rfqs = RFQ.objects.filter(buyer=request.user).order_by('-created_at')
    return render(request, 'ecommerce/my_rfqs.html', {'rfqs': rfqs})


@login_required
def place_order(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, is_active=True)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.buyer = request.user
            order.product = product
            order.total_amount = product.price * order.quantity
            order.currency = product.currency
            order.save()
            messages.success(request, f'Order placed! Reference your payment to Order #{order.pk}.')
            return redirect('my_orders')
    else:
        form = OrderForm()
    return render(request, 'ecommerce/place_order.html', {'form': form, 'product': product})


@login_required
def my_orders(request):
    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    return render(request, 'ecommerce/my_orders.html', {'orders': orders})
