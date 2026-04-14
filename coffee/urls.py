from django.urls import path
from . import views

urlpatterns = [
    path('', views.coffee_home, name='coffee_roasting'),
    path('products/', views.coffee_products, name='coffee_products'),
    path('order/<int:product_id>/', views.order_coffee, name='order_coffee'),
    path('my-orders/', views.my_coffee_orders, name='my_coffee_orders'),
]
