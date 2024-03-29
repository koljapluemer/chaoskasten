from ..models import *
from django.shortcuts import render, redirect
import os
from django.conf import settings as settings_conf

from django.contrib.auth import (
    authenticate, get_user_model, password_validation, login
)
from lazysignup.utils import is_lazy_user



def profile(request):
    try:
        request.user.profile
    except:
        return redirect('login')

    user = request.user
    profile = user.profile
    collection = profile.collection
    context = {}

    stripe.api_key = settings_conf.STRIPE_SECRET_KEY

    if not user.profile.has_free_account and not is_lazy_user(user):
        try: # this should only matter for testing
            if user.profile.stripeID != '1':
                created = stripe.Customer.retrieve(user.profile.stripeID).subscriptions.data[0]["created"]
                createdAsDate = datetime.utcfromtimestamp(created).strftime('%Y-%m-%d %H:%M')
                context['created'] = createdAsDate
        except:
            pass

    context['note_counter_all'] = profile.note_set.all().count() - 1
    context['note_counter_learning'] = profile.learningdata_set.all().count()
    context['note_counter_unlearned'] = profile.learningdata_set.filter(score__isnull=True).count()


    return render(request, 'pages/profile.html', context)

def voucher(request):
    user = request.user

    if request.method == 'POST':
        # skip the payment form when voucher is correct
        voucher_code = request.POST.get('voucher')
        print("VOUCHER", voucher_code)
        if voucher_code == "CHAOTISCH69":
            user.profile.has_free_account = True
            user.profile.save()
            return redirect('/notes')

    return render(request, 'registration/voucher.html')


def signup(request):

    stripe.api_key = settings_conf.STRIPE_SECRET_KEY

    if request.method == 'POST':
        print("SIGNUP STARTED")
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            voucher_code = request.POST.get('voucher')
            print("CODE", voucher_code)

            return redirect('/voucher')


    else:
        form = SignUpForm()

    return render(request, 'pages/signup.html', {'form': form})

def changeEmail(request):
    user = request.user
    if request.method == 'POST':
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            user.save()
            return redirect('/profile')
    else:
        form = EmailChangeForm()
    return render(request, 'registration/email_change.html', {'form': form})

def deleteUser(request):
    stripe.api_key = settings_conf.STRIPE_SECRET_KEY

    user = request.user
    if not user.profile.has_free_account:
        if user.profile.stripeID != '1':
            stripe.Customer.delete(user.profile.stripeID)
    user.delete()

    return redirect('/')
