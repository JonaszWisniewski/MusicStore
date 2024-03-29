import decimal
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product, Coupon
from .models import Cart, CartItem
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from users.models import Profile
from users.forms import ProfileUpdateForm
from products.forms import CouponCodeForm
from django.utils import timezone
from cart.forms import CartAddProductForm

# Create your views here.
def _cart_id(request):
	cart = request.session.session_key
	if not cart:
		cart = request.session.create()
	return cart

def view_cart(request, total=0, counter=0, cart_items = None, coupon_code=None, total_price_after_discount=0, get_discount=0, discount_percetange=0, discount_per_item=0, total_per_item=0, form=None):
	# form_qty = CartAddProductForm
	try:
		
		cart = Cart.objects.get(cart_id=_cart_id(request))
		cart_items = CartItem.objects.filter(cart=cart)

		for cart_item in cart_items:
			total += (cart_item.product.price * cart_item.quantity)
			counter += cart_item.quantity
			
		if request.method == 'POST':
			form = CouponCodeForm(request.POST)
			# form_qty = CartAddProductForm(request.POST)
			# if form_qty.is_valid():
			# 		qty = form_qty.cleaned_data.get('quantity')
			# 		cart_item.quantity = qty
			# else:
			# 		form_qty = CartAddProductForm()


			if form.is_valid():
					current_time = timezone.now()
					code = form.cleaned_data.get('code')
					coupon_obj = Coupon.objects.get(code=code)
					discount_decimal = decimal.Decimal(coupon_obj.discount / 100) # converts it into decimal
					discount_percetange = round(discount_decimal * 100)
					print(discount_percetange)
					if coupon_obj.valid_to >= current_time: # if coupon is valid date
						get_discount = round(discount_decimal * total, 2) # gets the discount for the whole cart
						print("discount", get_discount)
						total_price_after_discount = round(total - get_discount, 2) # total price of the discounted cart
						for cart_item in cart_items:
							# x = cart_item.product.price.amount
							# print("test: ", x)
							cart_item.discount_price = round(cart_item.product.price * discount_decimal, 2)
							print(type(cart_item.discount_price))
							# request.session['discount_pricee'][] = str(cart_item.discount_price)
							cart_item.save()
							print("cart item discount price", cart_item.discount_price)
							total_per_item = round(cart_item.discount_price * cart_item.quantity, 2)
							print("discount per item", cart_item.discount_price)

						total_price_after_discount = str(total_price_after_discount)
						print(total_price_after_discount)
						coupon_code = code
						
						
		else:
			form = CouponCodeForm()
					
		# coupon_code = request.session.get('coupon_code')
		# total_price_after_discount = request.session.get('discount_total')	
		
	except ObjectDoesNotExist:
		pass
	context = {'cart_items': cart_items, 'total': total, 'counter': counter, 'title': 'Cart', 'form': form, 'coupon_code': coupon_code, 
			'total_price_after_discount': total_price_after_discount, 'get_discount': get_discount, 'discount_per_item': discount_per_item, 'total_per_item': total_per_item, 'discount_percetange': discount_percetange}
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
					cart = cart,
					discount_price = 0.00
					
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


# @login_required
# def checkout(request, total=0, counter=0, cart_items = None):
# 	try:
# 		cart = Cart.objects.get(cart_id=_cart_id(request))
# 		cart_items = CartItem.objects.filter(cart=cart)
# 		for cart_item in cart_items:
# 			total += (cart_item.product.price * cart_item.quantity)
# 			counter += cart_item.quantity
# 	except ObjectDoesNotExist:
# 		pass
	
# 	profileForm = ProfileUpdateForm(instance=request.user.profile)
# 	context = {'cart_items': cart_items, 'total': total, 'counter': counter, 'title': 'Checkout', 'profileForm': profileForm}
# 	return render(request, 'cart/checkout.html', context)