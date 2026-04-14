from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TrainingProgram, Subscription


def programs_list(request):
    category = request.GET.get('category', '')
    programs = TrainingProgram.objects.filter(is_active=True)
    if category:
        programs = programs.filter(category=category)
    return render(request, 'training/programs.html', {
        'programs': programs,
        'selected_category': category,
        'categories': TrainingProgram.CATEGORY_CHOICES,
    })


def program_detail(request, slug):
    program = get_object_or_404(TrainingProgram, slug=slug, is_active=True)
    is_subscribed = False
    if request.user.is_authenticated:
        is_subscribed = Subscription.objects.filter(user=request.user, program=program).exists()
    return render(request, 'training/program_detail.html', {
        'program': program,
        'is_subscribed': is_subscribed,
    })


@login_required
def subscribe(request, slug):
    program = get_object_or_404(TrainingProgram, slug=slug)
    sub, created = Subscription.objects.get_or_create(user=request.user, program=program)
    if created:
        messages.success(request, f'You are now subscribed to "{program.title}".')
    else:
        messages.info(request, 'You are already subscribed to this program.')
    return redirect('program_detail', slug=slug)


@login_required
def my_programs(request):
    subscriptions = Subscription.objects.filter(user=request.user).select_related('program')
    return render(request, 'training/my_programs.html', {'subscriptions': subscriptions})
