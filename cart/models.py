from django.db import models
from products.models import Product
from djmoney.models.fields import MoneyField

class Cart(models.Model):
	cart_id = models.CharField(max_length=250, blank=True)
	date_added = models.DateField(auto_now_add=True)
	class Meta:
		db_table = 'Cart'
		ordering = ['date_added']

	def __str__(self):
		return self.cart_id

class CartItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	discount_price = MoneyField(max_digits=7, decimal_places=2, default_currency='USD')
	
	class Meta:
		db_table = 'CartItem'

	def sub_total(self):
		return self.product.price * self.quantity
	
	def discount_sub_total(self):
		return self.discount_price * self.quantity
	
	def total_after_discount(self):
		return self.sub_total() - self.discount_sub_total()

	def __str__(self):
		return self.product.name

