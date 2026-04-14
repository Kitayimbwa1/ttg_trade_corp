from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ExchangeRate, ForexTransaction
from .forms import ForexTransactionForm


def forex_home(request):
    rates = ExchangeRate.objects.all()
    return render(request, 'forex/forex_home.html', {'rates': rates})


@login_required
def exchange(request):
    rates = ExchangeRate.objects.all()
    if request.method == 'POST':
        form = ForexTransactionForm(request.POST)
        if form.is_valid():
            tx = form.save(commit=False)
            tx.user = request.user
            try:
                rate_obj = ExchangeRate.objects.get(
                    from_currency=tx.from_currency, to_currency=tx.to_currency
                )
                tx.rate_used = rate_obj.rate
                tx.amount_to = tx.amount_from * rate_obj.rate
            except ExchangeRate.DoesNotExist:
                tx.rate_used = 1
                tx.amount_to = tx.amount_from
            tx.save()
            messages.success(request, f'Transaction {tx.reference} submitted successfully.')
            return redirect('forex_history')
    else:
        form = ForexTransactionForm()
    return render(request, 'forex/exchange.html', {'form': form, 'rates': rates})


@login_required
def forex_history(request):
    transactions = ForexTransaction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'forex/history.html', {'transactions': transactions})
