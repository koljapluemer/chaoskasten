from django.shortcuts import render, redirect
import stripe

from django.conf import settings as cfg
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from main.models import Profile

# the stripe checkout form where the user inputs his credit card data
@csrf_exempt
def payment_form(request):
    stripe_public_key= cfg.STRIPE_PUBLIC_KEY
    stripe.api_key = cfg.STRIPE_SECRET_KEY

    # TODO: make this a setting
    domain_url = 'http://localhost:8000/'

    try:
        checkout_session = stripe.checkout.Session.create(
            customer=request.user.profile.stripeCustomerID,
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
        return render(request, 'registration/payment_form.html', {'stripe_public_key': stripe_public_key, 'stripeSessionID': checkout_session['id']})
    except Exception as e:
        # TODO: Redirect to error page
        return JsonResponse({'error': str(e)})


def success(request):
    return render(request, 'payment/success.html')


def cancel(request):
    return render(request, 'payment/cancel.html')


# actually confirm the payment
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
        )
        print(user.username + ' just subscribed.')

    return HttpResponse(status=200)
