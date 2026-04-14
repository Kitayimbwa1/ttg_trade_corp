from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/new/', views.add_product, name='add_product'),
    path('product/<slug:product_slug>/order/', views.place_order, name='place_order'),
    path('rfq/new/', views.submit_rfq, name='submit_rfq'),
    path('rfq/mine/', views.my_rfqs, name='my_rfqs'),
    path('orders/', views.my_orders, name='my_orders'),
]

# Avon Points URLs
from .avon_views import (avon_dashboard, avon_transactions, create_sell_order,
                        redeem_points, referral_info)

urlpatterns += [
    path('avon/', avon_dashboard, name='avon_dashboard'),
    path('avon/transactions/', avon_transactions, name='avon_transactions'),
    path('avon/sell-order/', create_sell_order, name='create_sell_order'),
    path('avon/redeem/', redeem_points, name='redeem_points'),
    path('avon/referrals/', referral_info, name='referral_info'),
]
