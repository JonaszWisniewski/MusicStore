import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect, render
from cart.models import Cart, CartItem
from cart.views import _cart_id
from orders.models import Order, OrderItems, OrderAddress
from django.conf import settings
from products.models import ProductsList
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from users.models import Profile

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request, pk): 

    get_order = get_object_or_404(Order, pk=pk) # gets the order if it exists

    if get_order.created_by == request.user and get_order.paid==False: # creates a checkout session if the order owner is equal to requesting user and order hasn't been paid for
        order = Order.objects.get(id=pk)
        a = request.user.profile.id
        print(request.user.profile.id)
        order_items = OrderItems.objects.filter(order=order)

        line_items = []
                        
        for order_item in order_items:
                                testval = order_item.discount_price.amount
                                print(testval)
                                unit_amount = (order_item.price.amount - testval) * 100
                                unit_amount = int(unit_amount)
                                print(type(unit_amount))
                                print(order_item.product.id)

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
                                        "order_id": pk,
                                        "user_id": request.user.id, # get the request user id from metadata
                                        "profile_id": request.user.profile.id
                                },
                        cancel_url=settings.SITE_URL + '/orders/{}'.format(pk)
                        
                )
        
        
        
        return redirect(checkout_session.url, code=303)
    else: # returns the user to order_history if order owner is not requesting user
        return redirect('orders:order_history')

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
        # Invalid payload returns status 400
                return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
        # Invalid signature returns status 400
                return HttpResponse(status=400)

        # Passed signature verification
        if event['type'] == 'checkout.session.completed':
    # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
                session = stripe.checkout.Session.retrieve(
                event['data']['object']['id'],
                expand=['line_items'],
                )
                
                order_id = session["metadata"]["order_id"]
                user = session["metadata"]["user_id"]
                profile_id = session["metadata"]["profile_id"] # retrieve the request user id from the session
                order_details = Order.objects.get(id=order_id)

                order_details.paid = True
           
                order_details.save()

                order_address = OrderAddress.objects.get(order=order_details)
                profile_obj = Profile.objects.get(id=profile_id)
                if order_details.is_default:
                        order_address.full_name = profile_obj.full_name
                        order_address.address1 = profile_obj.address1
                        order_address.address2 = profile_obj.address2
                        order_address.city = profile_obj.city
                        order_address.county = profile_obj.county
                        order_address.phone = profile_obj.phone
                        order_address.country = profile_obj.country
                        order_address.save()
                else:
                        order_address.full_name = "Tymoteusz"
                        order_address.address1 = "Address1"
                        order_address.address2 = "Address2"
                        order_address.city = "Cannes"
                        order_address.county = ""
                        order_address.phone = "123"
                        order_address.country = profile_obj.country
                        order_address.save()

                order_items = OrderItems.objects.filter(order=order_details)
                for order_item in order_items:
                                        
                                if not ProductsList.objects.filter(product=order_item.product, user_id=user).exists(): # check if an entry with the product_id and user_id not found in table
                                                product_list_insert = ProductsList.objects.create( # if not found create an object in ProductsList table
                                                product = order_item.product,
                                                user_id = user)
                                                product_list_insert.save()

                line_items = session.line_items
                # Fulfill the purchase...
                print(session)
                # context = {'order_details': order_details}
                return render(request, 'orders/order_history.html') # render the order_history.html template for order paid
        return HttpResponse(status=200) # if checkout session completed successful return status 200
