from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal
from .models import (AvonPointsAccount, AvonPointsTransaction, 
                     AvonPointsSellOrder, Order, PartnerCompany)

@login_required
def avon_dashboard(request):
    """Avon Points dashboard"""
    account, created = AvonPointsAccount.objects.get_or_create(user=request.user)
    
    # Get recent transactions
    transactions = account.transactions.all()[:10]
    
    # Get pending sell orders
    sell_orders = AvonPointsSellOrder.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Calculate earnings from orders
    total_from_purchases = Order.objects.filter(
        buyer=request.user,
        avon_points_awarded=True
    ).aggregate(total=Sum('avon_points_earned'))['total'] or 0
    
    total_from_referrals = Order.objects.filter(
        referred_by_user=request.user,
        avon_points_awarded=True
    ).aggregate(total=Sum('avon_points_earned'))['total'] or 0
    
    context = {
        'account': account,
        'transactions': transactions,
        'sell_orders': sell_orders,
        'total_from_purchases': total_from_purchases,
        'total_from_referrals': total_from_referrals,
    }
    return render(request, 'ecommerce/avon_dashboard.html', context)

@login_required
def avon_transactions(request):
    """View all Avon Points transactions"""
    account = get_object_or_404(AvonPointsAccount, user=request.user)
    transactions = account.transactions.all()
    
    return render(request, 'ecommerce/avon_transactions.html', {
        'account': account,
        'transactions': transactions,
    })

@login_required
def create_sell_order(request):
    """Create a sell order for Avon Points"""
    account, created = AvonPointsAccount.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        points_amount = Decimal(request.POST.get('points_amount', 0))
        quarter = request.POST.get('quarter', '')
        
        if points_amount > account.available_points:
            messages.error(request, 'Insufficient Avon Points balance.')
            return redirect('avon_dashboard')
        
        if points_amount < 100:
            messages.error(request, 'Minimum sell order is 100 Avon Points.')
            return redirect('avon_dashboard')
        
        # Default conversion rate (can be adjusted by admin)
        conversion_rate = Decimal('0.95')  # $0.95 per point
        usd_amount = points_amount * conversion_rate
        
        # Create sell order
        sell_order = AvonPointsSellOrder.objects.create(
            user=request.user,
            points_amount=points_amount,
            quarter=quarter,
            conversion_rate=conversion_rate,
            usd_amount=usd_amount,
            status='pending'
        )
        
        # Deduct points from available balance (pending execution)
        account.available_points -= points_amount
        account.save()
        
        messages.success(request, 
                        f'Sell order created for {points_amount} points. '
                        f'Estimated value: ${usd_amount:.2f} USD. '
                        f'Minimum 3-month execution period.')
        return redirect('avon_dashboard')
    
    quarters = AvonPointsSellOrder.QUARTER_CHOICES
    return render(request, 'ecommerce/create_sell_order.html', {
        'account': account,
        'quarters': quarters,
    })

@login_required
def redeem_points(request):
    """Redeem Avon Points for various uses"""
    account, created = AvonPointsAccount.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        redeem_type = request.POST.get('redeem_type', '')
        amount = Decimal(request.POST.get('amount', 0))
        
        if amount > account.available_points:
            messages.error(request, 'Insufficient Avon Points balance.')
            return redirect('avon_dashboard')
        
        # Process redemption based on type
        if redeem_type == 'insurance':
            purpose = 'Insurance premium payment'
        elif redeem_type == 'trading':
            purpose = 'Transfer to trading platform'
        elif redeem_type == 'real_estate':
            purpose = 'Real estate investment'
        elif redeem_type == 'withdrawal':
            purpose = 'Cash withdrawal'
        else:
            purpose = 'Other redemption'
        
        success = account.redeem_points(amount, purpose)
        
        if success:
            messages.success(request, 
                           f'Successfully redeemed {amount} Avon Points for {purpose}.')
        else:
            messages.error(request, 'Redemption failed. Please try again.')
        
        return redirect('avon_dashboard')
    
    return render(request, 'ecommerce/redeem_points.html', {'account': account})

@login_required
def referral_info(request):
    """Display referral information and stats"""
    # Get user's referral link/code
    referral_code = f"TTG{request.user.id:06d}"
    
    # Get orders referred by this user
    referred_orders = Order.objects.filter(referred_by_user=request.user)
    total_referred = referred_orders.count()
    total_points_earned = referred_orders.filter(
        avon_points_awarded=True
    ).aggregate(total=Sum('avon_points_earned'))['total'] or 0
    
    context = {
        'referral_code': referral_code,
        'total_referred': total_referred,
        'total_points_earned': total_points_earned,
        'referred_orders': referred_orders[:10],
    }
    return render(request, 'ecommerce/referral_info.html', context)
