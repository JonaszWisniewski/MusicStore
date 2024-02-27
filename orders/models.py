from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User


class Order(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    # email = models.EmailField(max_length=64, blank=True)
    created_by = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        # return 'Order {}'.format(self.id)
        return str(self.id)

    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.order_items.all())
    
    def get_items(self):
        return OrderItems.objects.filter(order=self)
    
class OrderItems(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.CharField(max_length=256)
    price = MoneyField(max_digits=7, decimal_places=2, default_currency='USD')
    quantity = models.PositiveIntegerField(default=1)
   

    def __str__(self):
        # return '{}'.format(self.id)
        return self.product
    
    def get_cost(self):
        return self.price * self.quantity