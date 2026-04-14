from django.contrib import admin
from .models import TrainingProgram, Subscription

@admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'duration_hours', 'certificate_fee_usd', 'is_active']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'program', 'status', 'completed', 'certificate_issued', 'subscribed_at']
    list_filter = ['status', 'certificate_issued', 'completed']
