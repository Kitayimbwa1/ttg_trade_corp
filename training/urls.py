from django.urls import path
from . import views

urlpatterns = [
    path('', views.programs_list, name='programs'),
    path('program/<slug:slug>/', views.program_detail, name='program_detail'),
    path('program/<slug:slug>/subscribe/', views.subscribe, name='subscribe'),
    path('my-programs/', views.my_programs, name='my_programs'),
]
