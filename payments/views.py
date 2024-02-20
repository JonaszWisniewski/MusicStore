from django.http import JsonResponse
from django.shortcuts import render, redirect
import stripe
from products.models import Product

stripe.api_key = 'sk_test_CKtP4w59YdQBvt2i8ehXHuQw00Nt6gF5Gg'


def landing_page_view(request):
    return redirect('cart:view_cart')

def create_checkout_session(self, request, *args, **kwargs):
    try:
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': product.price
                    
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
        )
        return JsonResponse({
            'id': checkout_session.id})
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)