from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('<int:pk>', views.detail, name='detail'),
    path('create/', views.create_order, name='create_order'),
    path('history/', views.order_history, name='order_history'),
    path('cancel/<int:order_id>', views.cancel_order, name='cancel_order'),

]