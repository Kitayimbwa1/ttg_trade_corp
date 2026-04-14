from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CoffeeProduct, CoffeeOrder, ProductionLevel

def coffee_home(request):
    """Coffee roasting business homepage"""
    products = CoffeeProduct.objects.filter(is_active=True)
    levels = ProductionLevel.objects.all()
    current_level = ProductionLevel.objects.filter(is_current=True).first()
    
    context = {
        'products': products,
        'levels': levels,
        'current_level': current_level,
    }
    return render(request, 'coffee/home.html', context)

def coffee_products(request):
    """List all coffee products"""
    products = CoffeeProduct.objects.filter(is_active=True)
    return render(request, 'coffee/products.html', {'products': products})

@login_required
def order_coffee(request, product_id):
    """Place a coffee order"""
    product = get_object_or_404(CoffeeProduct, pk=product_id, is_active=True)
    
    if request.method == 'POST':
        quantity_kg = float(request.POST.get('quantity_kg', 0))
        customer_type = request.POST.get('customer_type', 'consumer')
        delivery_address = request.POST.get('delivery_address', '')
        destination_country = request.POST.get('destination_country', 'UG')
        
        if quantity_kg > 0:
            order = CoffeeOrder.objects.create(
                customer=request.user,
                product=product,
                customer_type=customer_type,
                quantity_kg=quantity_kg,
                unit_price=product.price_per_kg,
                total_amount=quantity_kg * product.price_per_kg,
                delivery_address=delivery_address,
                destination_country=destination_country
            )
            messages.success(request, f'Coffee order {order.order_number} placed successfully!')
            return redirect('my_coffee_orders')
        else:
            messages.error(request, 'Please enter a valid quantity.')
    
    return render(request, 'coffee/order.html', {'product': product})

@login_required
def my_coffee_orders(request):
    """View user's coffee orders"""
    orders = CoffeeOrder.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'coffee/my_orders.html', {'orders': orders})
