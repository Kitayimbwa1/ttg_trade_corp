from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import InsuranceProduct, InsurancePolicy
from .forms import InsurancePolicyForm

def insurance_products(request):
    products = InsuranceProduct.objects.filter(is_active=True)
    return render(request, 'insurance/products.html', {'products': products})

@login_required
def purchase_insurance(request, product_id):
    product = get_object_or_404(InsuranceProduct, pk=product_id, is_active=True)
    if request.method == 'POST':
        form = InsurancePolicyForm(request.POST)
        if form.is_valid():
            policy = form.save(commit=False)
            policy.user = request.user
            policy.product = product
            policy.save()
            return redirect('insurance_policies')
    else:
        form = InsurancePolicyForm()
    return render(request, 'insurance/purchase.html', {'form': form, 'product': product})

@login_required
def my_policies(request):
    policies = InsurancePolicy.objects.filter(user=request.user)
    return render(request, 'insurance/my_policies.html', {'policies': policies})
