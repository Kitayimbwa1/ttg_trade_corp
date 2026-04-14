from django.db import models
from django.contrib.auth.models import User


class TraderProfile(models.Model):
    MARKET_CHOICES = [('local', 'Local Market'), ('international', 'International Market')]
    DURATION_CHOICES = [('long_term', 'Long Term'), ('short_term', 'Short Term')]
    COUNTRY_CHOICES = [
        ('CA', 'Canada'), ('UG', 'Uganda'), ('NL', 'Netherlands'),
        ('JP', 'Japan'), ('KE', 'Kenya'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trader_profile')
    phone_number = models.CharField(max_length=20)
    country_of_residence = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    market_type = models.CharField(max_length=20, choices=MARKET_CHOICES, default='local')
    trading_duration = models.CharField(max_length=20, choices=DURATION_CHOICES, default='short_term')
    business_description = models.TextField(help_text="Brief description of your trading activity")
    declaration = models.TextField(help_text="Your declaration and agreement with T&TG Trade Corp")
    declaration_file = models.FileField(upload_to='declarations/', blank=True, null=True)
    national_id_front = models.ImageField(upload_to='kyc/ids/', blank=True, null=True)
    national_id_back = models.ImageField(upload_to='kyc/ids/', blank=True, null=True)
    selfie = models.ImageField(upload_to='kyc/selfies/', blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)
    profile_link_slug = models.SlugField(unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_company = models.BooleanField(default=False)
    company_name = models.CharField(max_length=200, blank=True)
    has_certificate = models.BooleanField(default=False)
    is_international_eligible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_market_type_display()}"

    def save(self, *args, **kwargs):
        if not self.profile_link_slug:
            from django.utils.text import slugify
            base = slugify(self.user.get_full_name() or self.user.username)
            slug = base
            i = 1
            while TraderProfile.objects.filter(profile_link_slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.profile_link_slug = slug
        super().save(*args, **kwargs)


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"
