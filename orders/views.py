from datetime import datetime, timezone
from django.shortcuts import render, redirect, get_object_or_404
from users.forms import ProfileUpdateForm
from .models import Order, OrderItems
from cart.models import Cart, CartItem
from cart.views import _cart_id
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

@login_required
def create_order(request, total=0, counter=0, cart_items=None):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart)
            
            print(cart_items)
            
            if cart_items:
                order_details = Order.objects.create(created_by=request.user)
                
                order_details.save()
        
    
        
            # cart = Cart.objects.get(cart_id = _cart_id(request))
            # cart_items = CartItem.objects.filter(cart=cart)
            
            for order_items in cart_items:
                order_item = OrderItems.objects.create(
                    product = order_items.product.name,
                    price = order_items.product.price,
                    quantity = order_items.quantity,
                    order = order_details)
                    
                total += (order_items.quantity * order_items.product.price)
                counter += order_items.quantity
                order_item.save() # saves the order
                

                order_items.delete() # clears the basket that existed with items
        except ObjectDoesNotExist:
            pass
        
        profileForm = ProfileUpdateForm(instance=request.user.profile)
        context = {'cart_items': cart_items, 'total': total, 'profileForm': profileForm, 'title': 'My Order', 'counter': counter}
        return render(request, 'orders/order.html', context)

@login_required
def order_history(request):
    if request.user.is_authenticated:
        # email = str(request.user.email)
        order_details = Order.objects.filter(created_by=request.user)
    
        context = {'order_details': order_details, 'title': 'All Orders'}

    return render(request, 'orders/order_history.html', context)

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_date = order.created_date
    current_date = datetime.now(timezone.utc)
    date_difference = current_date - order_date
    difference_in_mins = date_difference.total_seconds() / 60.0
    if difference_in_mins <= 150 and order.paid == False:
        order.delete()
        messages.success(request, ("The order has been deleted successfully"))
    else:
        messages.success(request, ("It is too late to cancel this order"))
    return redirect('orders:order_history')


@login_required
def detail(request, pk):
    
    order_details = get_object_or_404(Order, pk=pk)
    if order_details.created_by == request.user or request.user.is_staff:
        order_details = Order.objects.filter(pk=pk)
    
        return render(request, 'orders/order_detail.html', 
                  {'order_details': order_details, 'title': 'View order'})
    else:
        return redirect('orders:order_history')
                   





