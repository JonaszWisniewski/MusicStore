from .models import Cart, CartItem
from .views import _cart_id

def cart(request):
	item_count = 0
	# if request.user.is_staff: # if admin then return 0 otherwise return number of items in cart
	# 	return {}
	# else:
	try:
			cart = Cart.objects.filter(cart_id=_cart_id(request))
			cart_items = CartItem.objects.all().filter(cart=cart[:1])
			for cart_item in cart_items:
				item_count += cart_item.quantity
	except Cart.DoesNotExist:
			item_count = 0
	return dict(item_count = item_count)