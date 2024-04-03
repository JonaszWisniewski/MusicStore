from datetime import datetime, timezone
import decimal
from django.shortcuts import render, redirect, get_object_or_404
from users.forms import ProfileUpdateForm
from .models import Order, OrderItems
from cart.models import Cart, CartItem
from cart.views import _cart_id
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.paginator import Paginator
from products.models import Coupon

@login_required
def create_order(request, total=0, counter=0, cart_items=None, discount_price=0, total_discount=0):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart)
            
            print(cart_items)
            
            if cart_items:
                order_details = Order.objects.create(created_by=request.user)
                order_details.save()

            for order_items in cart_items:
                order_item = OrderItems.objects.create(
                    product = order_items.product,
                    price = order_items.product.price,
                    quantity = order_items.quantity,
                    discount_price = order_items.discount_price, #pulls the discount price from the cart
                    order = order_details)
                
                total += (order_items.quantity * order_items.product.price)
                counter += order_items.quantity
                total_discount += (order_items.quantity * order_items.discount_price)
                
                order_item.save() # saves the order

                order_items.delete() # clears the basket that existed with items
            
            # for item in cart_items:
            #     discount_price = item.discount_price   
        except ObjectDoesNotExist:
            pass
        # del request.session['discount_pricee']
        # profileForm = ProfileUpdateForm(instance=request.user.profile)
        context = {'cart_items': cart_items, 'total': total, 'title': 'My Order', 'counter': counter, 'discount_price': discount_price, 'total_discount': total_discount}
        return render(request, 'orders/order.html', context)

@login_required
def order_history(request):
    if request.user.is_authenticated:
        # email = str(request.user.email)
        order_details = Order.objects.filter(created_by=request.user)

        page = Paginator(order_details, 3)

        page_list = request.GET.get('page')
      

        page = page.get_page(page_list)

        context = {'page': page, 'title': 'All Orders'}

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
        profileForm = ProfileUpdateForm(instance=request.user.profile)
    
        return render(request, 'orders/order_detail.html', 
                  {'order_details': order_details, 'profileForm': profileForm, 'title': 'Order {}'.format(pk)})
    else:
        return redirect('orders:order_history')
                   





