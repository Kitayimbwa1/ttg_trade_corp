from django.db import models
from django.contrib.auth.models import User


class TrainingProgram(models.Model):
    CATEGORY_CHOICES = [
        ('farming', 'Modern & Tech Farming'),
        ('enterprise', 'Mid-Market Enterprise Programs'),
        ('finance', 'Financial Services & Investments'),
    ]
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='training/thumbnails/', blank=True, null=True)
    duration_hours = models.PositiveIntegerField(default=1)
    certificate_fee_usd = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    is_free_to_watch = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('expired', 'Expired'), ('cancelled', 'Cancelled')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    program = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE, related_name='subscriptions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    subscribed_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    certificate_paid = models.BooleanField(default=False)
    certificate_issued = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'program')

    def __str__(self):
        return f"{self.user} — {self.program}"
