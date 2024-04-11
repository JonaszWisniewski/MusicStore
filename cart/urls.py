from django.urls import path
from . import views
 
app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_product_to_cart, name='add_product_to_cart'),
    path('remove/<int:product_id>/', views.remove_product_from_cart, name='remove_product_from_cart'),
    path('clear/', views.clear_cart, name='clear_cart'),
]