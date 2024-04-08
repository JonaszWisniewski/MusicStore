from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.loginview, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('change/', views.change_password, name='change_password'),

]