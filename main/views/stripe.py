from django.shortcuts import render, redirect
import stripe

from django.conf import settings as cfg
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from main.models import Profile

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': cfg.STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = cfg.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                # success_url=domain_url + 'success/session_id={CHECKOUT_SESSION_ID}',
                success_url=domain_url + 'success/',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': cfg.STRIPE_PRICE_ID,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


# @login_required
def success(request):
    return render(request, 'payment/success.html')


# @login_required
def cancel(request):
    return render(request, 'payment/cancel.html')


# actually confirm the payment and create a user profile

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = cfg.STRIPE_SECRET_KEY
    endpoint_secret = cfg.STRIPE_ENDPOINT_SECRET
    payload = request.body
    if 'HTTP_STRIPE_SIGNATURE' in request.META:
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    else:
        sig_header = "no sig header found, something went wrong"
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')

        # Get the user and create a new StripeCustomer
        user = User.objects.get(id=client_reference_id)
        Profile.objects.create(
            user=user,
            stripeCustomerID=stripe_customer_id,
            stripeSubscriptionID=stripe_subscription_id,
        )
        print(user.username + ' just subscribed.')

    return HttpResponse(status=200)
