"""
T&TG Trade Corp — Django Signals
Auto-fire notifications when key model events occur.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver


# ── TRADER PROFILE STATUS CHANGE ──
@receiver(post_save, sender='core.TraderProfile')
def notify_profile_status(sender, instance, created, **kwargs):
    from notifications.models import Notification
    if created:
        Notification.send(
            user=instance.user,
            title="Registration Received",
            message="Your trader registration has been submitted and is under review. We'll notify you within 2–3 business days.",
            notif_type='registration',
            link='/dashboard/',
        )
    elif instance.status == 'approved':
        Notification.send(
            user=instance.user,
            title="Account Approved ✓",
            message="Congratulations! Your trader account has been approved. You can now list products and access the marketplace.",
            notif_type='registration',
            link='/dashboard/',
        )
    elif instance.status == 'rejected':
        Notification.send(
            user=instance.user,
            title="Application Update",
            message="Your registration could not be approved at this time. Please contact us for more information.",
            notif_type='registration',
            link='/contact/',
        )


# ── ORDER PLACED ──
@receiver(post_save, sender='ecommerce.Order')
def notify_order(sender, instance, created, **kwargs):
    from notifications.models import Notification
    if created:
        Notification.send(
            user=instance.buyer,
            title=f"Order #{instance.pk} Placed",
            message=f"Your order for \"{instance.product.title}\" has been placed. Total: {instance.currency} {instance.total_amount}. Please complete your payment via {instance.get_payment_method_display()}.",
            notif_type='order',
            link='/trade/orders/',
        )
        # Also notify seller
        Notification.send(
            user=instance.product.seller,
            title=f"New Order Received",
            message=f"You received an order for \"{instance.product.title}\" (Qty: {instance.quantity}) from {instance.buyer.get_full_name()}.",
            notif_type='order',
            link='/dashboard/',
        )
    elif instance.status in ('paid', 'shipped', 'delivered'):
        Notification.send(
            user=instance.buyer,
            title=f"Order #{instance.pk} — {instance.get_status_display()}",
            message=f"Your order for \"{instance.product.title}\" is now {instance.get_status_display().lower()}.",
            notif_type='order',
            link='/trade/orders/',
        )


# ── FOREX TRANSACTION ──
@receiver(post_save, sender='forex.ForexTransaction')
def notify_forex(sender, instance, created, **kwargs):
    from notifications.models import Notification
    if created:
        Notification.send(
            user=instance.user,
            title=f"Forex Request — {instance.reference}",
            message=f"Your exchange request of {instance.amount_from} {instance.from_currency} → {instance.to_currency} has been received. Reference: {instance.reference}.",
            notif_type='forex',
            link='/forex/history/',
        )


# ── TRAINING SUBSCRIPTION ──
@receiver(post_save, sender='training.Subscription')
def notify_subscription(sender, instance, created, **kwargs):
    from notifications.models import Notification
    if created:
        Notification.send(
            user=instance.user,
            title=f"Enrolled: {instance.program.title}",
            message=f"You're now enrolled in \"{instance.program.title}\". Complete the course and pay the certificate fee (${instance.program.certificate_fee_usd}) to earn your qualification.",
            notif_type='training',
            link='/training/my-programs/',
        )
    elif instance.certificate_issued:
        Notification.send(
            user=instance.user,
            title="Certificate Issued 🎓",
            message=f"Your Certificate of Completion for \"{instance.program.title}\" has been issued. You now have access to international market trading, priority employment, and secondary shareholding eligibility.",
            notif_type='certificate',
            link='/training/my-programs/',
        )
