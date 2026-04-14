from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TraderProfile, ContactMessage
from .forms import TraderRegistrationForm, ContactForm, TraderProfileUpdateForm


def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def services(request):
    return render(request, 'core/services.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent. We will respond shortly.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = TraderRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration submitted! Your application is under review.')
            return redirect('dashboard')
    else:
        form = TraderRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def dashboard(request):
    try:
        profile = request.user.trader_profile
    except TraderProfile.DoesNotExist:
        profile = None
    return render(request, 'core/dashboard.html', {'profile': profile})

@login_required
def profile_view(request, slug):
    profile = get_object_or_404(TraderProfile, profile_link_slug=slug)
    return render(request, 'core/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    try:
        profile = request.user.trader_profile
    except TraderProfile.DoesNotExist:
        return redirect('register')
    if request.method == 'POST':
        form = TraderProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('dashboard')
    else:
        form = TraderProfileUpdateForm(instance=profile)
    return render(request, 'core/edit_profile.html', {'form': form, 'profile': profile})

def operations(request):
    return render(request, 'core/operations.html')

def tv_program(request):
    episodes_data = [
        {'num': '01', 'title': 'Global Grain Trade: East Africa to Europe',
         'desc': 'How Ugandan and Kenyan farmers are exporting directly to Dutch buyers through digital platforms.',
         'img': 'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=600&q=70',
         'category': 'Farming', 'duration': '28 min', 'region': 'Uganda · Netherlands'},
        {'num': '02', 'title': 'USD/UGX Outlook — Q1 2026 Analysis',
         'desc': 'A deep dive into Ugandan shilling performance, inflation drivers, and cross-border remittance trends.',
         'img': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=600&q=70',
         'category': 'Finance', 'duration': '22 min', 'region': 'Canada · Uganda'},
        {'num': '03', 'title': 'Building a Mid-Market Company from Toronto',
         'desc': 'Tom Ssembiito on the journey of founding T&TG Trade Corp and the vision behind a multi-country enterprise.',
         'img': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&q=70',
         'category': 'Enterprise', 'duration': '35 min', 'region': 'Canada'},
        {'num': '04', 'title': 'Drone Farming in East Africa',
         'desc': 'How precision agriculture technology is transforming smallholder farming in Kenya and Uganda.',
         'img': 'https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?w=600&q=70',
         'category': 'Farming', 'duration': '31 min', 'region': 'Kenya · Uganda'},
        {'num': '05', 'title': 'Japan–Africa Trade Corridor Opening',
         'desc': 'Opportunities and challenges in direct Japanese business partnerships with East African exporters.',
         'img': 'https://images.unsplash.com/photo-1536098561742-ca998e48cbcc?w=600&q=70',
         'category': 'Enterprise', 'duration': '26 min', 'region': 'Japan · Kenya'},
        {'num': '06', 'title': 'Mobile Money: The Backbone of African Trade',
         'desc': 'MTN MoMo, M-Pesa, and Airtel Money — how mobile payments are enabling a new era of cross-border commerce.',
         'img': 'https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=600&q=70',
         'category': 'Finance', 'duration': '19 min', 'region': 'Uganda · Kenya'},
    ]
    return render(request, 'core/tv_program.html', {'episodes_data': episodes_data})

def invest(request):
    return render(request, 'core/invest.html')

def error_404(request, exception=None):
    return render(request, 'errors/404.html', status=404)

def error_500(request):
    return render(request, 'errors/500.html', status=500)
