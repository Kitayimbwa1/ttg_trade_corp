from django.urls import path
from . import views

urlpatterns = [
    path('', views.insurance_products, name='insurance_products'),
    path('purchase/<int:product_id>/', views.purchase_insurance, name='purchase_insurance'),
    path('my-policies/', views.my_policies, name='insurance_policies'),
]
