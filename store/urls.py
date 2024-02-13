from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
# from .forms import LoginForm

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
]
