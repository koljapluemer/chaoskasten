from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings as settings_conf
import stripe

def payment(request):
    # Stripe
    stripe.api_key = settings_conf.STRIPE_SECRET_KEY

    session = stripe.checkout.Session.create(
        customer=request.user.profile.stripeID,
        payment_method_types=['card'],
        subscription_data={
            'items': [{
                'plan': 'plan_Gu4VwViHu775Pj',
            }],
        },
        success_url='http://chaoskasten.com/notes',
        cancel_url='https://chaoskasten.com/signup'
    )
    return render(request, 'payment.html', {'stripeSessionID': session.id, 'stripe_pk': settings_conf.STRIPE_PUBLIC_KEY})

@csrf_exempt
def webhook(request):
    stripe.api_key = settings_conf.STRIPE_SECRET_KEY

    # You can find your endpoint's secret in your webhook settings
    endpoint_secret = settings_conf.STRIPE_WEBHOOK


    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    body = json.loads(payload)
    customerID = body['data']['object']['customer']
    print(customerID)
    print(Profile.objects.get(stripeID=customerID).user.username + " has paid")

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

        # Fulfill the purchase...
        handle_checkout_session(session)

    return HttpResponse(status=200)
