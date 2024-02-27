from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [
    path('checkout/<int:pk>', views.checkout, name='checkout'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
]