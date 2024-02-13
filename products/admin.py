from django.contrib import admin

from .models import Category, Product
from users.models import Profile


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Profile)


