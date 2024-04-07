from django.contrib import admin

from .models import Category, Product, Coupon, ProductsList
from users.models import Profile


admin.site.register(Category)
admin.site.register(Coupon)
admin.site.register(Product)
admin.site.register(ProductsList)
admin.site.register(Profile)


