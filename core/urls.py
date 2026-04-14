from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('operations/', views.operations, name='operations'),
    path('invest/', views.invest, name='invest'),
    path('tv/', views.tv_program, name='tv_program'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/<slug:slug>/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
