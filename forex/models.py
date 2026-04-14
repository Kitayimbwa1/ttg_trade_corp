from django.db import models
from django.contrib.auth.models import User


class ExchangeRate(models.Model):
    from_currency = models.CharField(max_length=5)
    to_currency = models.CharField(max_length=5)
    rate = models.DecimalField(max_digits=14, decimal_places=6)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('from_currency', 'to_currency')

    def __str__(self):
        return f"{self.from_currency} → {self.to_currency} @ {self.rate}"


class ForexTransaction(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')]
    TYPE_CHOICES = [('buy', 'Buy'), ('sell', 'Sell')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forex_transactions')
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    from_currency = models.CharField(max_length=5)
    to_currency = models.CharField(max_length=5)
    amount_from = models.DecimalField(max_digits=14, decimal_places=2)
    amount_to = models.DecimalField(max_digits=14, decimal_places=2)
    rate_used = models.DecimalField(max_digits=14, decimal_places=6)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reference = models.CharField(max_length=100, unique=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} | {self.from_currency}→{self.to_currency} | {self.amount_from}"

    def save(self, *args, **kwargs):
        if not self.reference:
            import uuid
            self.reference = f"TTG-FX-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)
