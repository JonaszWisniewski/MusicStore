from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [
    path('payments/', views.landing_page_view, name='landing_page_view'),
    path('create_checkout_session/<pk>/', views.create_checkout_session, name='create_checkout_session'),
]