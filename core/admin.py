from django.contrib import admin
from .models import TraderProfile, ContactMessage


@admin.register(TraderProfile)
class TraderProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'country_of_residence', 'market_type', 'status', 'created_at']
    list_filter = ['status', 'market_type', 'country_of_residence']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    actions = ['approve_profiles', 'reject_profiles']

    def approve_profiles(self, request, queryset):
        queryset.update(status='approved')
    approve_profiles.short_description = "Approve selected profiles"

    def reject_profiles(self, request, queryset):
        queryset.update(status='rejected')
    reject_profiles.short_description = "Reject selected profiles"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read']
