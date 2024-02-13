from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('<int:pk>', views.detail, name='detail'),
    path('new/', views.new_product, name='new_product'),
    path('<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('<int:pk>/edit/', views.edit_product, name='edit_product'),
]

