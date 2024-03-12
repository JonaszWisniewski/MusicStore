import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect, render
from cart.models import Cart, CartItem
from cart.views import _cart_id
from orders.models import Order, OrderItems
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse, HttpResponse



@login_required
def checkout(request, pk): #315
    stripe.api_key = settings.STRIPE_SECRET_KEY
#     cart = Cart.objects.get(cart_id=_cart_id(request)) #retrieving the cart session
#     print(cart)
#     cart_items = CartItem.objects.filter(cart=cart) #retrieving the cart items
#     print(cart_items)
    
    order = Order.objects.get(id=pk)
    
    order_items = OrderItems.objects.filter(order=order)
    print(order_items)
    line_items = []
                
    for order_item in order_items:
                        unit_amount = int(order_item.price.amount * 100)
                        line_items.append({
                                'price_data': {
                                        'currency': 'usd',
                                        'unit_amount': unit_amount,
                                        'product_data': {
                                                'name': order_item.product,
                                                # add images in the future, unable at the moment as stripe is unable to access local django server
            
                                        },
                                },
                                'quantity': order_item.quantity
                        }),
                        
                        
                        
    checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                payment_method_types=['card'],
                mode='payment',
                success_url=settings.SITE_URL,
                metadata={
                                "order_id": pk
                        },
                cancel_url=settings.SITE_URL + '/orders/{}'.format(pk)
                
            )
    
    return redirect(checkout_session.url, code=303)


@csrf_exempt
def stripe_webhook(request):
        
        payload = request.body
        
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        event = None

        try:
                event = stripe.Webhook.construct_event(
                        payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
                )
        except ValueError as e:
        # Invalid payload
                return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
        # Invalid signature
                return HttpResponse(status=400)

        # Passed signature verification
        if event['type'] == 'checkout.session.completed':
    # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
                session = stripe.checkout.Session.retrieve(
                event['data']['object']['id'],
                expand=['line_items'],
                )
                
                order_id = session["metadata"]["order_id"]
                
                order_details = Order.objects.get(id=order_id)
                print(order_details)
                order_details.paid = True
           
                order_details.save()
                line_items = session.line_items
                # Fulfill the purchase...
                print(session)
                return render(request, 'orders/order_history', {'order_details': order_details})
        return HttpResponse(status=200)




    



