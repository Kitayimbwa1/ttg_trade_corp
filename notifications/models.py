from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    TYPE_CHOICES = [
        ('registration',  'Registration Update'),
        ('order',         'Order Update'),
        ('rfq',           'RFQ Update'),
        ('forex',         'Forex Transaction'),
        ('training',      'Training Update'),
        ('certificate',   'Certificate Issued'),
        ('general',       'General'),
    ]

    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notif_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='general')
    title      = models.CharField(max_length=200)
    message    = models.TextField()
    link       = models.CharField(max_length=300, blank=True)
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_notif_type_display()}] {self.title} → {self.user.username}"

    @classmethod
    def send(cls, user, title, message, notif_type='general', link=''):
        """Convenience factory — creates a notification for one user."""
        return cls.objects.create(
            user=user, title=title, message=message,
            notif_type=notif_type, link=link,
        )

    @classmethod
    def send_bulk(cls, users, title, message, notif_type='general', link=''):
        """Send the same notification to multiple users."""
        objs = [
            cls(user=u, title=title, message=message,
                notif_type=notif_type, link=link)
            for u in users
        ]
        cls.objects.bulk_create(objs)
