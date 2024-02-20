from datetime import datetime, timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItems
from products.models import Product
from cart.models import Cart, CartItem
from cart.views import _cart_id
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

@login_required
def create_order(request, total=0, cart_items=None):
    if request.user.is_authenticated:
        email = str(request.user.email)
        order_details = Order.objects.create(email=email)
        order_details.save()
    
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart)
            for order_items in cart_items:
                order_item = OrderItems.objects.create(
                    product = order_items.product.name,
                    price = order_items.product.price,
                    quantity = order_items.quantity,
                    order = order_details)
                total += (order_items.quantity * order_items.product.price)
                order_item.save() # saves the order
                order_items.delete() # clears the basket that existed with items
        except ObjectDoesNotExist:
            pass
        context = {'cart_items': cart_items, 'total':total}
        return render(request, 'orders/order.html', context)

@login_required
def order_history(request):
    if request.user.is_authenticated:
        email = str(request.user.email)
        order_details = Order.objects.filter(email=email)
    
        context = {'order_details': order_details}

        return render(request, 'orders/order_history.html', context)

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_date = order.created_date
    current_date = datetime.now(timezone.utc)
    date_difference = current_date - order_date
    difference_in_mins = date_difference.total_seconds() / 60.0
    if difference_in_mins <= 30:
        order.delete()
        messages.success(request, ("Order has been deleted successfully"))
    else:
        messages.success(request, ("It is too late to cancel this order"))
    return redirect('orders:order_history')





