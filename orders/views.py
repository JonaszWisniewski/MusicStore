from datetime import datetime, timezone
from django.shortcuts import render, redirect, get_object_or_404
from users.forms import ProfileUpdateForm
from .models import Order, OrderItems, OrderAddress
from cart.models import Cart, CartItem
from cart.views import _cart_id
from orders.forms import AddressUpdateForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.paginator import Paginator
from products.models import Coupon
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def create_order(request, total=0, counter=0, cart_items=None, discount_price=0, total_discount=0):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart)
            
            print(cart_items)
            
            if cart_items:
                order_details = Order.objects.create(created_by=request.user)
                order_details.save() # returns the id of the order


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

                # order_address = OrderAddress.objects.create(
                # order = order_details,
                # profile = request.user.profile
                # )
                # order_address.save()
            
        except ObjectDoesNotExist:
            pass
        # profileForm = ProfileUpdateForm(instance=request.user.profile)
        context = {'cart_items': cart_items, 'total': total, 'title': 'My Order', 'counter': counter, 'discount_price': discount_price, 'total_discount': total_discount}
        return render(request, 'orders/order.html', context)

@login_required
def order_history(request):
    if request.user.is_authenticated:
        email = str(request.user.email)
        order_details = Order.objects.filter(created_by=request.user)
        paginator = Paginator(order_details, 3)
        page = request.GET.get('page')

        try:
            order_details = paginator.page(page)
        except PageNotAnInteger:
            if order_details:
                order_details = paginator.page(1)
        
        except EmptyPage:
            order_details = paginator.page(paginator.num_pages)


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
        get_order_id = Order.objects.get(pk=pk)
        is_default = request.POST.getlist('is_default')
        if not is_default:
            is_default = False
        if is_default == ['True']:
            is_default = True

        order_details.is_default = is_default
      
        order_default = Order.objects.get(pk=pk)
        order_default.is_default = is_default
        print(order_default.is_default)
        order_default.save()
        profileForm = ProfileUpdateForm(instance=request.user.profile)
        if request.method == 'POST':
            orderForm = AddressUpdateForm(request.POST)
            testing123 = orderForm.save(commit=False)
            testing123.order_id = pk
            testing123.created_by_id = request.user.id
            if not Order.objects.filter(id=pk, created_by_id=request.user.id).exists():
                testing123.save()
                
        else:
            orderForm = AddressUpdateForm()
    
        return render(request, 'orders/order_detail.html', 
                  {'order_details': order_details, 'orderForm': orderForm, 'profileForm': profileForm, 'title': 'Order {}'.format(pk)})
    else:
        return redirect('orders:order_history')
                   
# def detail(request, pk): # saves into profile information
#     order_details = get_object_or_404(Order, pk=pk)
#     if order_details.created_by == request.user or request.user.is_staff:
#             order_details = Order.objects.filter(pk=pk)

#             if request.method == 'POST':
#                 profileForm = ProfileUpdateForm(request.POST, instance=request.user.profile)
#                 if profileForm.is_valid():
#                     profileForm.save()
#             else:
#                 profileForm = ProfileUpdateForm(instance=request.user.profile)


#             return render(request, 'orders/order_detail.html', 
#                         {'order_details': order_details, 'profileForm': profileForm, 'title': 'Order {}'.format(pk)})
#     else:
#         return redirect('orders:order_history')




