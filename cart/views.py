from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import Cart, CartItem
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from users.models import Profile
from users.forms import ProfileUpdateForm

# Create your views here.
def _cart_id(request):
	cart = request.session.session_key
	if not cart:
		cart = request.session.create()
	return cart

def view_cart(request, total=0, counter=0, cart_items = None):
	try:
		cart = Cart.objects.get(cart_id=_cart_id(request))
		cart_items = CartItem.objects.filter(cart=cart)
		for cart_item in cart_items:
			total += (cart_item.product.price * cart_item.quantity)
			counter += cart_item.quantity
	except ObjectDoesNotExist:
		pass
	context = {'cart_items': cart_items, 'total': total, 'counter': counter, 'title': "Cart"}
	return render(request, 'cart/cart.html', context)

def add_product_to_cart(request, product_id):
	product = Product.objects.get(id=product_id)
	try:
		cart = Cart.objects.get(cart_id=_cart_id(request))
	except Cart.DoesNotExist:
		cart = Cart.objects.create(
				cart_id = _cart_id(request)
			)
		cart.save()
	try:
		cart_item = CartItem.objects.get(product=product, cart=cart)
		cart_item.quantity +=1
		cart_item.save()
		
	except CartItem.DoesNotExist:
		cart_item = CartItem.objects.create(
					product = product,
					quantity = 1,
					cart = cart
			)
		cart_item.save()
	return redirect('cart:view_cart')

def remove_product_from_cart(request, product_id):
	cart = Cart.objects.get(cart_id=_cart_id(request))
	product = get_object_or_404(Product, id=product_id)
	cart_item = CartItem.objects.get(product=product, cart=cart)
	if cart_item.quantity > 1:
		cart_item.quantity -= 1
		cart_item.save()
	else:
		cart_item.delete()
	return redirect('cart:view_cart')

def clear_cart(request):
	cart = Cart.objects.get(cart_id=_cart_id(request))
	cart_items = CartItem.objects.filter(cart=cart)
	for cart_item in cart_items:
		cart_item.delete()
	return redirect('cart:view_cart')

@login_required
def checkout(request, total=0, counter=0, cart_items = None):
	try:
		cart = Cart.objects.get(cart_id=_cart_id(request))
		cart_items = CartItem.objects.filter(cart=cart)
		for cart_item in cart_items:
			total += (cart_item.product.price * cart_item.quantity)
			counter += cart_item.quantity
	except ObjectDoesNotExist:
		pass
	
	profileForm = ProfileUpdateForm(instance=request.user.profile)
	context = {'cart_items': cart_items, 'total': total, 'counter': counter, 'title': "Checkout", 'profileForm': profileForm}
	return render(request, 'cart/checkout.html', context)