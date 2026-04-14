from django.urls import path
from . import views

urlpatterns = [
    path('', views.forex_home, name='forex_home'),
    path('exchange/', views.exchange, name='exchange'),
    path('history/', views.forex_history, name='forex_history'),
]
