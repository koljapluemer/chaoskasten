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

    domain_url = cfg.DOMAIN_URL

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
